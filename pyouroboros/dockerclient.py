from time import sleep
from logging import getLogger
from docker import DockerClient
from docker.errors import DockerException, APIError, NotFound

from pyouroboros.helpers import set_properties


class Docker(object):
    def __init__(self, socket, config, data_manager, notification_manager):
        self.config = config
        self.socket = socket
        self.client = DockerClient(base_url=socket, tls=self.config.docker_tls_verify)
        self.data_manager = data_manager
        self.data_manager.total_updated[self.socket] = 0
        self.logger = getLogger()
        self.monitored = self.monitor_filter()

        self.notification_manager = notification_manager

    def get_running(self):
        """Return running container objects list, except ouroboros itself"""
        running_containers = []
        try:
            for container in self.client.containers.list(filters={'status': 'running'}):
                if self.config.self_update:
                    running_containers.append(container)
                else:
                    try:
                        if 'ouroboros' not in container.image.tags[0]:
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
        running_containers = self.get_running()
        monitored_containers = []

        for container in running_containers:
            ouro_label = container.labels.get('com.ouroboros.enable', False)
            # if labels enabled, use the label. 'true/yes' trigger monitoring.
            if self.config.label_enable and ouro_label:
                if ouro_label.lower() in ["true", "yes"]:
                    monitored_containers.append(container)
                elif ouro_label.lower() in ["false", "no"]:
                    continue
                else:
                    self.logger.error('Malformed container enable label value in container \"%s\" (\"%s\").', container.name, ouro_label)
                    continue
            elif not self.config.labels_only and self.config.monitor and container.name in self.config.monitor \
                    and container.name not in self.config.ignore:
                    monitored_containers.append(container)
            elif not self.config.labels_only and container.name not in self.config.ignore:
                    monitored_containers.append(container)

        self.data_manager.monitored_containers[self.socket] = len(monitored_containers)
        self.data_manager.set(self.socket)

        return monitored_containers

    def pull(self, image_object):
        """Docker pull image tag/latest"""
        image = image_object
        try:
            tag = image.tags[0]
        except IndexError:
            self.logger.error('Malformed or missing tag. Skipping...')
            raise ConnectionError
        if self.config.latest and image.tags[0][-6:] != 'latest':
            if ':' in tag:
                split_tag = tag.split(':')
                if len(split_tag) == 2:
                    if '/' not in split_tag[1]:
                        tag = split_tag[0]
                else:
                    tag = ':'.join(split_tag[:-1])
            tag = f'{tag}:latest'

        self.logger.debug('Checking tag: %s', tag)
        try:
            if self.config.dry_run:
                registry_data = self.client.images.get_registry_data(tag)
                return registry_data
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
                self.logger.critical("Couldn't find an image on docker.com for %s. Local Build?", image.tags[0])
                raise ConnectionError
            elif ('pull access' or 'TLS handshake') in str(e):
                self.logger.critical("Couldn't pull. Skipping. Error: %s", e)
                raise ConnectionError

    def update_containers(self):
        updated_count = 0
        updated_container_tuples = []
        depends_on_list = []
        self.monitored = self.monitor_filter()

        if not self.monitored:
            self.logger.info('No containers are running or monitored on %s', self.socket)

        me_list = [c for c in self.client.api.containers() if 'ouroboros' in c['Names'][0].strip('/')]
        if len(me_list) > 1:
            self.update_self(count=2, me_list=me_list)

        for container in self.monitored:
            current_image = container.image

            shared_image = [uct for uct in updated_container_tuples if uct[1].id == current_image.id]
            if shared_image:
                latest_image = shared_image[0][2]
            else:
                try:
                    latest_image = self.pull(current_image)
                except ConnectionError:
                    continue

            if self.config.dry_run:
                # Ugly hack for repo digest
                repo_digest_id = current_image.attrs['RepoDigests'][0].split('@')[1]
                if repo_digest_id != latest_image.id:
                    self.logger.info('dry run : %s would be updated', container.name)
                continue

            # If current running container is running latest image
            if current_image.id != latest_image.id:
                updated_container_tuples.append(
                    (container, current_image, latest_image)
                )

                if container.name in ['ouroboros', 'ouroboros-updated']:
                    self.data_manager.total_updated[self.socket] += 1
                    self.data_manager.add(label=container.name, socket=self.socket)
                    self.data_manager.add(label='all', socket=self.socket)
                    self.notification_manager.send(container_tuples=updated_container_tuples,
                                                   socket=self.socket, kind='update')
                    self.update_self(old_container=container, new_image=latest_image, count=1)

                self.logger.info('%s will be updated', container.name)

                # Get container list to restart after update complete
                depends_on = container.labels.get('com.ouroboros.depends-on', False)
                if depends_on:
                    depends_on_list.extend([name.strip() for name in depends_on.split(',')])
                # new container dict to create new container from
                new_config = set_properties(old=container, new=latest_image)

                self.logger.debug('Stopping container: %s', container.name)
                stop_signal = container.labels.get('com.ouroboros.stop-signal', False)
                if stop_signal:
                    try:
                        container.kill(signal=stop_signal)
                    except APIError as e:
                        self.logger.error('Cannot kill container using signal %s. stopping normally. Error: %s',
                                          stop_signal, e)
                        container.stop()
                else:
                    container.stop()

                self.logger.debug('Removing container: %s', container.name)
                try:
                    container.remove()
                except NotFound as e:
                    self.logger.error("Could not remove container. Error: %s", e)

                created = self.client.api.create_container(**new_config)
                new_container = self.client.containers.get(created.get("Id"))
                new_container.start()

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

        if depends_on_list:
            depends_on_containers = []
            for name in list(set(depends_on_list)):
                try:
                    depends_on_containers.append(self.client.containers.get(name))
                except NotFound:
                    self.logger.error("Could not find dependant container %s on socket %s. Ignoring", name, self.socket)

            if depends_on_containers:
                for container in depends_on_containers:
                    self.logger.debug('Restarting dependant container %s', container.name)
                    container.restart()

        if updated_count > 0:
            self.notification_manager.send(container_tuples=updated_container_tuples, socket=self.socket, kind='update')

    def update_self(self, count=None, old_container=None, me_list=None, new_image=None):
        if count == 2:
            self.logger.debug('God im messy... cleaning myself up.')
            old_me_id = me_list[0]['Id'] if me_list[0]['Created'] < me_list[1]['Created'] else me_list[1]['Id']
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
            me_created = self.client.api.create_container(**new_config)
            new_me = self.client.containers.get(me_created.get("Id"))
            new_me.start()
            self.logger.debug('If you strike me down, I shall become more powerful than you could possibly imagine')
            self.logger.debug('https://bit.ly/2VVY7GH')
            sleep(30)
