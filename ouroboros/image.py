import docker

client = docker.from_env()

def pull_latest(image):
    """Return tag of latest image pulled"""
    return client.images.pull(image.tags[0].split(':')[0] + ':latest')

def is_up_to_date(old_sha, new_sha):
    """Returns boolean if old and new image digests match"""
    return old_sha == new_sha

def remove(old_image):
    """Deletes old image after container is updated"""
    return client.images.remove(old_image)