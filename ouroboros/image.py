import docker
import main
import logging

def pull_latest(image):
    """Return tag of latest image pulled"""
    latest_image = image.tags[0].split(':')[0] + ':latest'
    logging.debug(('Pulling image: {}').format(latest_image))
    return main.client.images.pull(latest_image)

def is_up_to_date(old_sha, new_sha):
    """Returns boolean if old and new image digests match"""
    return old_sha == new_sha

def remove(old_image):
    """Deletes old image after container is updated"""
    logging.info(('Removing image: {}').format(old_image.tags[0]))
    return main.client.images.remove(old_image.id)