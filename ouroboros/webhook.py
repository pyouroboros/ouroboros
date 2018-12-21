import logging
import json
import requests

log = logging.getLogger(__name__)


def post(urls, container_name, old_sha, new_sha):
    for url in urls:
        try:
            payload = {'text': f'Container: {container_name} updated from {old_sha} to {new_sha}'}
            requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'user-agent': 'ouroboros'})
        except requests.ConnectionError:
            log.error(f'Unable to connect to {url}. Skipping webhook notification.')
        except requests.exceptions.MissingSchema:
            log.error(f'{url} is an invalid URL. Skipping webhook notification.')
        except(Exception) as e:
            log.error(e)
