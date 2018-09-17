import docker

client = docker.from_env()

def running():
    """Return list of running containers"""
    return client.containers.list()

def running_properties():
    """Return container object"""
    return docker.APIClient(base_url='unix://var/run/docker.sock').containers()