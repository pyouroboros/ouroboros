from time import sleep
from logging import getLogger
from docker import DockerClient, tls
from os.path import isdir, isfile, join
from docker.errors import DockerException, APIError, NotFound

from pyouroboros.helpers import set_properties, remove_sha_prefix, get_digest


class Docker(object):
    def __init__(self, socket, config, data_manager, notification_manager):
        self.config = config
        self.socket = socket
        self.client = self.connect()
        self.data_manager = data_manager
        self.logger = getLogger()

        self.notification_manager = notification_manager

    def connect(self):
        if self.config.docker_tls:
            try:
                cert_paths = {
                    'cert_top_dir': '/etc/docker/certs.d/',
                    'clean_socket': self.socket.split('//')[1]
                }
                cert_paths['cert_dir'] = join(cert_paths['cert_top_dir'], cert_paths['clean_socket'])
                cert_paths['cert_files'] = {
                    'client_cert': join(cert_paths['cert_dir'], 'client.cert'),
                    'client_key': join(cert_paths['cert_dir'], 'client.key'),
                    'ca_crt': join(cert_paths['cert_dir'], 'ca.crt')
                }

                if not isdir(cert_paths['cert_dir']):
                    self.logger.error('%s is not a valid cert folder', cert_paths['cert_dir'])
                    raise ValueError

                for cert_file in cert_paths['cert_files'].values():
                    if not isfile(cert_file):
                        self.logger.error('%s does not exist', cert_file)
                        raise ValueError

                tls_config = tls.TLSConfig(
                    ca_cert=cert_paths['cert_files']['ca_crt'],
                    verify=cert_paths['cert_files']['ca_crt'] if self.config.docker_tls_verify else False,
                    client_cert=(cert_paths['cert_files']['client_cert'], cert_paths['cert_files']['client_key'])
                )
                client = DockerClient(base_url=self.socket, tls=tls_config)
            except ValueError:
                self.logger.error('Invalid Docker TLS config for %s, reverting to unsecured', self.socket)
                client = DockerClient(base_url=self.socket)
        else:
            client = DockerClient(base_url=self.socket)

        return client


class BaseImageObject(object):
    def __init__(self, docker_client):
        self.docker = docker_client
        self.logger = self.docker.logger
        self.config = self.docker.config
        self.client = self.docker.client
        self.socket = self.docker.socket
        self.data_manager = self.docker.data_manager
        self.data_manager.total_updated[self.socket] = 0
        self.notification_manager = self.docker.notification_manager

    def _pull(self, tag):
        """Docker pull image tag"""
        self.logger.debug('Checking tag: %s', tag)
        try:
            if self.config.dry_run:
                # The authentication doesn't work with this call
                # See bugs https://github.com/docker/docker-py/issues/2225
                return self.client.images.get_registry_data(tag)
            else:
                if self.config.auth_json:
                    return_image = self.client.images.pull(tag, auth_config=self.config.auth_json)
                else:
                    return_image = self.client.images.pull(tag)
                return return_image
        except APIError as e:
            if '<html>' in str(e):
                self.logger.debug("Docker api issue. Ignoring")
                raise ConnectionError
            elif 'unauthorized' in str(e):
                if self.config.dry_run:
                    self.logger.error('dry run : Upstream authentication issue while checking %s. See: '
                                      'https://github.com/docker/docker-py/issues/2225', tag)
                    raise ConnectionError
                else:
                    self.logger.critical("Invalid Credentials. Exiting")
                    exit(1)
            elif 'Client.Timeout' in str(e):
                self.logger.critical(
                    "Couldn't find an image on docker.com for %s. Local Build?", tag)
                raise ConnectionError
            elif ('pull access' or 'TLS handshake') in str(e):
                self.logger.critical("Couldn't pull. Skipping. Error: %s", e)
                raise ConnectionError


class Container(BaseImageObject):
    mode = 'container'

    def __init__(self, docker_client):
        super().__init__(docker_client)
        self.monitored = self.monitor_filter()

    # Container sub functions
    def stop(self, container):
        self.logger.debug('Stopping container: %s', container.name)
        stop_signal = container.labels.get('com.ouroboros.stop_signal', False)
        if stop_signal:
            try:
                container.kill(signal=stop_signal)
            except APIError as e:
                self.logger.error('Cannot kill container using signal %s. stopping normally. Error: %s',
                                  stop_signal, e)
                container.stop()
        else:
            container.stop()

    def remove(self, container):
        self.logger.debug('Removing container: %s', container.name)
        try:
            container.remove()
        except NotFound as e:
            self.logger.error("Could not remove container. Error: %s", e)
            return

    def recreate(self, container, latest_image):
        new_config = set_properties(old=container, new=latest_image)

        self.stop(container)
        self.remove(container)

        created = self.client.api.create_container(**new_config)
        new_container = self.client.containers.get(created.get("Id"))

        # connect the new container to all networks of the old container
        for network_name, network_config in container.attrs['NetworkSettings']['Networks'].items():
            network = self.client.networks.get(network_config['NetworkID'])
            try:
                network.disconnect(new_container.id, force=True)
            except APIError:
                pass
            new_network_config = {
                'container': new_container,
                'aliases': network_config['Aliases'],
                'links': network_config['Links']
            }
            if network_config['IPAMConfig']:
                new_network_config.update(
                    {
                        'ipv4_address': network_config['IPAddress'],
                        'ipv6_address': network_config['GlobalIPv6Address']
                    }
                )
            try:
                network.connect(**new_network_config)
            except APIError as e:
                if any(err in str(e) for err in ['user configured subnets', 'user defined networks']):
                    if new_network_config.get('ipv4_address'):
                        del new_network_config['ipv4_address']
                    if new_network_config.get('ipv6_address'):
                        del new_network_config['ipv6_address']
                    network.connect(**new_network_config)
                else:
                    self.logger.error('Unable to attach updated container to network "%s". Error: %s', network.name, e)

        new_container.start()

    def pull(self, current_tag):
        """Docker pull image tag"""
        tag = current_tag
        if not tag:
            self.logger.error('Missing tag. Skipping...')
            raise ConnectionError
        elif ':' not in tag:
            tag = f'{tag}:latest'
        return self._pull(tag)

    # Filters
    def running_filter(self):
        """Return running container objects list, except ouroboros itself"""
        running_containers = []
        try:
            for container in self.client.containers.list(filters={'status': 'running'}):
                if self.config.self_update:
                    running_containers.append(container)
                else:
                    try:
                        if 'ouroboros' not in container.image.tags[0]:
                            if container.attrs['HostConfig']['AutoRemove']:
                                self.logger.debug("Skipping %s due to --rm property.", container.name)
                            else:
                                running_containers.append(container)
                    except IndexError:
                        self.logger.error("%s has no tags.. you should clean it up! Ignoring.", container.id)
                        continue

        except DockerException:
            self.logger.critical("Can't connect to Docker API at %s", self.config.docker_socket)
            exit(1)

        return running_containers

    def monitor_filter(self):
        """Return filtered running container objects list"""
        running_containers = self.running_filter()
        monitored_containers = []

        for container in running_containers:
            ouro_label = container.labels.get('com.ouroboros.enable', False)
            # if labels enabled, use the label. 'true/yes' trigger monitoring.
            if self.config.label_enable and ouro_label:
                if ouro_label.lower() in ["true", "yes"]:
                    monitored_containers.append(container)
                else:
                    continue
            elif not self.config.labels_only:
                if self.config.monitor:
                    if container.name in self.config.monitor and container.name not in self.config.ignore:
                        monitored_containers.append(container)
                elif container.name not in self.config.ignore:
                    monitored_containers.append(container)

        self.data_manager.monitored_containers[self.socket] = len(monitored_containers)
        self.data_manager.set(self.socket)

        return monitored_containers

    # Socket Functions
    def self_check(self):
        if self.config.self_update:
            me_list = [container for container in self.client.containers.list() if 'ouroboros' in container.name]
            if len(me_list) > 1:
                self.update_self(count=2, me_list=me_list)

    def socket_check(self):
        depends_on_names = []
        hard_depends_on_names = []
        updateable = []
        self.monitored = self.monitor_filter()

        if not self.monitored:
            self.logger.info('No containers are running or monitored on %s', self.socket)
            return

        for container in self.monitored:
            current_image = container.image
            current_tag = container.attrs['Config']['Image']
            shared_image = [uct for uct in updateable if uct[1].id == current_image.id]
            if shared_image:
                latest_image = shared_image[0][2]
            else:
                try:
                    latest_image = self.pull(current_tag)
                except ConnectionError:
                    continue
            try:
                if current_image.id != latest_image.id:
                    updateable.append((container, current_image, latest_image))
                else:
                    continue
            except AttributeError:
                self.logger.error("Issue detecting %s's image tag. Skipping...", container.name)

            # Get container list to restart after update complete
            depends_on = container.labels.get('com.ouroboros.depends_on', False)
            hard_depends_on = container.labels.get('com.ouroboros.hard_depends_on', False)
            if depends_on:
                depends_on_names.extend([name.strip() for name in depends_on.split(',')])
            if hard_depends_on:
                hard_depends_on_names.extend([name.strip() for name in hard_depends_on.split(',')])

        hard_depends_on_containers = []
        hard_depends_on_names = list(set(hard_depends_on_names))
        for name in hard_depends_on_names:
            try:
                hard_depends_on_containers.append(self.client.containers.get(name))
            except NotFound:
                self.logger.error("Could not find dependant container %s on socket %s. Ignoring", name, self.socket)

        depends_on_containers = []
        depends_on_names = list(set(depends_on_names))
        depends_on_names = [name for name in depends_on_names if name not in hard_depends_on_names]
        for name in depends_on_names:
            try:
                depends_on_containers.append(self.client.containers.get(name))
            except NotFound:
                self.logger.error("Could not find dependant container %s on socket %s. Ignoring", name, self.socket)

        return updateable, depends_on_containers, hard_depends_on_containers

    def update(self):
        updated_count = 0
        try:
            updateable, depends_on_containers, hard_depends_on_containers = self.socket_check()
        except TypeError:
            return

        for container in depends_on_containers + hard_depends_on_containers:
            self.stop(container)

        for container, current_image, latest_image in updateable:
            if self.config.dry_run:
                # Ugly hack for repo digest
                repo_digest_id = current_image.attrs['RepoDigests'][0].split('@')[1]
                if repo_digest_id != latest_image.id:
                    self.logger.info('dry run : %s would be updated', container.name)
                continue

            if container.name in ['ouroboros', 'ouroboros-updated']:
                self.data_manager.total_updated[self.socket] += 1
                self.data_manager.add(label=container.name, socket=self.socket)
                self.data_manager.add(label='all', socket=self.socket)
                self.notification_manager.send(container_tuples=updateable,
                                               socket=self.socket, kind='update')
                self.update_self(old_container=container, new_image=latest_image, count=1)

            self.logger.info('%s will be updated', container.name)

            self.recreate(container, latest_image)

            if self.config.cleanup:
                try:
                    self.client.images.remove(current_image.id)
                except APIError as e:
                    self.logger.error("Could not delete old image for %s, Error: %s", container.name, e)
            updated_count += 1

            self.logger.debug("Incrementing total container updated count")

            self.data_manager.total_updated[self.socket] += 1
            self.data_manager.add(label=container.name, socket=self.socket)
            self.data_manager.add(label='all', socket=self.socket)

        for container in depends_on_containers:
            # Reload container to ensure it isn't referencing the old image
            container.reload()
            container.start()

        for container in hard_depends_on_containers:
            self.recreate(container, container.image)

        if updated_count > 0:
            self.notification_manager.send(container_tuples=updateable, socket=self.socket, kind='update')

    def update_self(self, count=None, old_container=None, me_list=None, new_image=None):
        if count == 2:
            self.logger.debug('God im messy... cleaning myself up.')
            old_me_id = me_list[0].id if me_list[0].attrs['Created'] < me_list[1].attrs['Created'] else me_list[1].id
            old_me = self.client.containers.get(old_me_id)
            old_me_image_id = old_me.image.id

            old_me.stop()
            old_me.remove()

            self.client.images.remove(old_me_image_id)
            self.logger.debug('Ahhh. All better.')

            self.monitored = self.monitor_filter()
        elif count == 1:
            self.logger.debug('I need to update! Starting the ouroboros ;)')
            self_name = 'ouroboros-updated' if old_container.name == 'ouroboros' else 'ouroboros'
            new_config = set_properties(old=old_container, new=new_image, self_name=self_name)
            try:
                me_created = self.client.api.create_container(**new_config)
                new_me = self.client.containers.get(me_created.get("Id"))
                new_me.start()
                self.logger.debug('If you strike me down, I shall become '
                                  'more powerful than you could possibly imagine.')
                self.logger.debug('https://bit.ly/2VVY7GH')
                sleep(30)
            except APIError as e:
                self.logger.error("Self update failed.")
                self.logger.error(e)


class Service(BaseImageObject):
    mode = 'service'

    def __init__(self, docker_client):
        super().__init__(docker_client)
        self.monitored = self.monitor_filter()

    def monitor_filter(self):
        """Return filtered service objects list"""
        services = self.client.services.list(filters={'label': 'com.ouroboros.enable'})

        monitored_services = []

        for service in services:
            ouro_label = service.attrs['Spec']['Labels'].get('com.ouroboros.enable')
            if not self.config.label_enable or ouro_label.lower() in ["true", "yes"]:
                monitored_services.append(service)

        self.data_manager.monitored_containers[self.socket] = len(monitored_services)
        self.data_manager.set(self.socket)

        return monitored_services

    def pull(self, tag):
        """Docker pull image tag"""
        return self._pull(tag)

    def update(self):
        updated_service_tuples = []
        self.monitored = self.monitor_filter()

        if not self.monitored:
            self.logger.info('No services monitored')

        for service in self.monitored:
            image_string = service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image']
            if '@' in image_string:
                tag = image_string.split('@')[0]
                sha256 = remove_sha_prefix(image_string.split('@')[1])
            else:
                self.logger.error('No image SHA for %s. Skipping', image_string)
                continue

            try:
                latest_image = self.pull(tag)
            except ConnectionError:
                continue

            latest_image_sha256 = get_digest(latest_image)
            self.logger.debug('Latest sha256 for %s is %s', tag, latest_image_sha256)

            if sha256 != latest_image_sha256:
                if self.config.dry_run:
                    # Ugly hack for repo digest
                    self.logger.info('dry run : %s would be updated', service.name)
                    continue

                updated_service_tuples.append(
                    (service, sha256[-10:], latest_image)
                )

                if 'ouroboros' in service.name and self.config.self_update:
                    self.data_manager.total_updated[self.socket] += 1
                    self.data_manager.add(label=service.name, socket=self.socket)
                    self.data_manager.add(label='all', socket=self.socket)
                    self.notification_manager.send(container_tuples=updated_service_tuples,
                                                   socket=self.socket, kind='update', mode='service')

                self.logger.info('%s will be updated', service.name)
                service.update(image=f"{tag}@sha256:{latest_image_sha256}")

                self.data_manager.total_updated[self.socket] += 1
                self.data_manager.add(label=service.name, socket=self.socket)
                self.data_manager.add(label='all', socket=self.socket)

        if updated_service_tuples:
            self.notification_manager.send(
                container_tuples=updated_service_tuples,
                socket=self.socket,
                kind='update',
                mode='service'
            )
