import logging
import main

def pull_latest(image):
    """Return tag of latest image pulled"""
    latest_image = image['RepoTags'][0].split(':')[0] + ':latest'
    logging.debug(('Pulling image: {}').format(latest_image))
    main.api_client.pull(latest_image)
    return main.api_client.inspect_image(latest_image)

def is_up_to_date(old_sha, new_sha):
    """Returns boolean if old and new image digests match"""
    return old_sha == new_sha

def remove(old_image):
    """Deletes old image after container is updated"""
    logging.info(('Removing image: {}').format(old_image['RepoTags'][0]))
    return main.api_client.remove_image(old_image)