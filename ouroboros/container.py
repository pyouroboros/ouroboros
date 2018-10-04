import logging
import main
import cli

class NewContainerProperties:
    def __init__(self, old_container, new_image):
        """
        Store object for spawning new container in place of the one with outdated image
        """
        self.name = get_name(old_container)
        self.image = new_image
        self.command = old_container['Config']['Cmd']
        self.host_config = old_container['HostConfig']
        self.labels = old_container['Config']['Labels']
        self.detach = True
        self.entrypoint = old_container['Config']['Entrypoint']

def running():
    """Return all running container objects list"""
    running_containers = []
    try:
        for container in main.api_client.containers():
            if container['State'] == 'running':
                running_containers.append(main.api_client.inspect_container(container))
        return running_containers
    except:
        logging.critical(('Can\'t connect to Docker API at {}').format(main.api_client.base_url))

def to_monitor():
    """Return container object list"""
    container_list = []
    for container in running():
        if len(cli.monitor) == 0:
            container_list.append(get_name(container))
        elif container['Name'] in cli.monitor:
            container_list.append(get_name(container))
    logging.debug(('Monitoring containers: {}').format(container_list))
    return running()

def get_name(container_object):
    """Parse out first name of container"""
    return container_object['Name'].replace('/','')

def stop(container_object):
    """Stop out of date container"""
    logging.debug(('Stopping container: {}').format(get_name(container_object)))
    return main.api_client.stop(container_object)

def remove(container_object):
    """Remove out of date container"""
    logging.debug(('Removing container: {}').format(get_name(container_object)))
    return main.api_client.remove_container(container_object)

def create_new_container(config):
    """Create new container with latest image"""
    return main.api_client.create_container(**config)

def start(container_object):
    """Start newly created container with latest image"""
    logging.debug(('Starting container: {}').format(container_object['Id']))
    return main.api_client.start(container_object)
