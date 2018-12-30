import logging
import json
import requests

log = logging.getLogger(__name__)


def post(urls, container_name, old_sha, new_sha):
    """POST webhook for notifications"""
    for url in urls:
        try:
            payload = {'text': f'Container: {container_name} updated from {old_sha} to {new_sha}'}
            return requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'user-agent': 'ouroboros'})
        except(Exception) as e:
            log.error(e)
