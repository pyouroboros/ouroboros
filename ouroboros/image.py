from os import environ
import logging
from docker.errors import DockerException

log = logging.getLogger(__name__)


def check_credentials():
    """Returns dict of credentials if environment variable 'REPO_USER' and 'REPO_PASS' are set"""
    if environ.get('REPO_USER') and environ.get('REPO_PASS'):
        return {'username': environ['REPO_USER'],
                'password': environ['REPO_PASS']}
    return {}


def pull_latest(image, keep_tag, api_client):
    """Return tag of latest image pulled"""
    latest_image = image['RepoTags'][0].split(':')[0] + ':latest'
    if keep_tag:
        latest_image = image['RepoTags'][0]
    log.debug(f'Pulling image: {latest_image}')
    api_client.pull(latest_image, auth_config=check_credentials())
    return api_client.inspect_image(latest_image)


def is_up_to_date(old_sha, new_sha):
    """Returns boolean if old and new image digests match"""
    return old_sha == new_sha


def remove(old_image, api_client):
    """Deletes old image after container is updated"""
    log.info(f"Removing image: {old_image['RepoTags'][0]}")
    result = {}
    try:
        result = api_client.remove_image(old_image)
    except DockerException as e:
        log.critical(f"Could not clean up image: {old_image['RepoTags'][0]}, reason: \n{e}")
    return result
