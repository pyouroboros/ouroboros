import docker

client = docker.from_env()

def pull_latest(image):
    """Return tag of latest image pulled. Will be a version, not latest"""
    return client.images.pull(image.tags[0].split(':')[0] + ':latest')
