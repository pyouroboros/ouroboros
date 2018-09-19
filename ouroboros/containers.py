import docker

client = docker.from_env()

class NewContainerProperties:
    def __init__(self, old_container, new_image):
        """
        Store object for spawning new container in place of the one with outdated image
        """
        self.name = old_container['Names'][0].replace('/','')
        self.image = new_image
        self.old_image_id = old_container['ImageID']
        self.command = old_container['Command']
        self.ports = old_container['Ports']
        self.labels = old_container['Labels']
        self.network = next(iter(old_container['NetworkSettings']['Networks']))
        self.mounts = old_container['Mounts']
        self.detach = True
        if 'Entrypoint' in old_container:
            self.entrypoint = old_container["Entrypoint"]

def running_properties():
    """Return container object"""
    return docker.APIClient(base_url='unix://var/run/docker.sock').containers()
