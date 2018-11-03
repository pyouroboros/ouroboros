import logging
from docker.errors import DockerException

log = logging.getLogger(__name__)


def new_container_properties(old_container, new_image):
    """Store object for spawning new container in place of the one with outdated image"""
    props = {
        'name': get_name(old_container),
        'image': new_image,
        'command': old_container['Config']['Cmd'],
        'host_config': old_container['HostConfig'],
        'labels': old_container['Config']['Labels'],
        'entrypoint': old_container['Config']['Entrypoint'],
        'environment': old_container['Config']['Env']
    }
    return props


def running(api_client):
    """Return running container objects list, except ouroboros itself"""
    running_containers = []
    try:
        for container in api_client.containers(filters={'status': 'running'}):
            if 'ouroboros' not in container['Image']:
                running_containers.append(
                    api_client.inspect_container(container))
    except DockerException:
        log.critical(
            f'Can\'t connect to Docker API at {api_client.base_url}')
    return running_containers


def to_monitor(monitor=None, ignore=None, api_client=None):
    """Return filtered running container objects list"""

    running_containers = running(api_client)

    if monitor:
        running_containers = [container for container in running_containers if get_name(container) in monitor]

    if ignore:
        log.info(f'Ignoring container(s): {", ".join(ignore)}')
        running_containers = [container for container in running_containers if get_name(container) not in ignore]

    return running_containers


def get_name(container_object):
    """Parse out first name of container"""
    return container_object['Name'].replace('/', '')


def stop(container_object, api_client):
    """Stop out of date container"""
    log.debug(f'Stopping container: {get_name(container_object)}')
    api_client.stop(container_object)


def remove(container_object, api_client):
    """Remove out of date container"""
    log.debug(f'Removing container: {get_name(container_object)}')
    api_client.remove_container(container_object)


def create_new(config, api_client):
    """Create new container with latest image"""
    return api_client.create_container(**config)


def start(container_object, api_client):
    """Start newly created container with latest image"""
    log.debug(f"Starting container: {container_object['Id']}")
    api_client.start(container_object)
