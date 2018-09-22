import docker

client = docker.APIClient(base_url='unix://var/run/docker.sock')

class NewContainerProperties:
    def __init__(self, old_container, new_image):
        """
        Store object for spawning new container in place of the one with outdated image
        """
        self.name = old_container['Names'][0].replace('/','')
        self.image = new_image
        self.command = old_container['Command']
        self.ports = self.get_container_ports(old_container['Ports'])
        self.host_config = client.create_host_config(port_bindings=self.create_host_config(old_container['Ports']))
        self.labels = old_container['Labels']
        self.networking_config = { next(iter(old_container['NetworkSettings']['Networks'])): '' }
        #self.volumes = old_container['Mounts']
        self.detach = True
        if 'Entrypoint' in old_container:
            self.entrypoint = old_container['Entrypoint']

    def get_container_ports(self, port_list):
        """Get exposed container ports"""
        container_port_list = []
        for i in port_list:
            container_port_list.append(i['PrivatePort'])
        return container_port_list

    def create_host_config(self, port_list):
        """Create host_config port bindings dictionary"""
        port_bindings = {}
        for i in port_list:
            port_bindings.update({ i['PrivatePort']:i['PublicPort'] })
        return port_bindings

def running_properties():
    """Return container object"""
    return client.containers()

def stop(container_id):
    """Stop out of data container"""
    client.stop(container_id)

def remove(container_id):
    """Remove out of date container"""
    client.remove_container(container_id)

def create_new_container(config):
    """Create new container with latest image"""
    return client.create_container(**config)

def start(container_id):
    """Start newly created container with latest image"""
    client.start(container_id)
