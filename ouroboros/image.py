import docker
client = docker.from_env()

def pull_latest(image):
    """Return the names:tags of latest image pulled"""
    return client.images.pull(image.tags[0].split(':')[0] + ':latest')
