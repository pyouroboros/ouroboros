import docker

client = docker.from_env()

def running():
    """Get list of running containers"""
    return client.containers.list()