import docker

client = docker.from_env()

class new_container_properties:
    def __init__(self, old_container, new_image):
        self.name = old_container['Names'][0].replace('/','')
        self.image = new_image
        self.old_image_id = old_container['ImageID']
        self.command = old_container['Command']
        self.ports = old_container['Ports']
        self.labels = old_container['Labels']
        self.network = next(iter(old_container['NetworkSettings']['Networks']))
        self.mounts = old_container['Mounts']
        if old_container["Entrypoint"]:
            self.entrypoint = old_container["Entrypoint"]

def running():
    """Return list of running containers"""
    return client.containers.list()

def running_properties():
    """Return container object"""
    return docker.APIClient(base_url='unix://var/run/docker.sock').containers()