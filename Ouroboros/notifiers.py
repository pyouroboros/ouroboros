import requests

from datetime import datetime
from logging import getLogger
from requests.exceptions import RequestException


class NotificationManager(object):
    def __init__(self, config, monitored_count):
        self.config = config
        self.monitored_count = monitored_count
        self.logger = getLogger()

    def send(self, updated_count, container_tuples):
        if self.config.webhook_urls:
            formatted_json = self.format(updated_count, container_tuples)
            self.post(formatted_json)

    def format(self, updated_count, container_tuples):
        now = str(datetime.now()).replace(" ", "T")
        if self.config.webhook_type == 'slack':
            text = "Containers Monitored: {}\n".format(self.monitored_count)
            text += "Containers Updated: {}\n".format(updated_count)
            for container, old_image, new_image in container_tuples:
                text += "{} updated from {} to {}\n".format(
                    container.name,
                    old_image.short_id.split(":")[1],
                    new_image.short_id.split(":")[1]
                )
            text += now
            json = {"text": text}
            return json

        elif self.config.webhook_type == 'discord':
            json = {
                "embeds": [
                    {
                        "title": "Ouroboros has updated containers!",
                        "description": "Breakdown:",
                        "color": 316712,
                        "timestamp": now,
                        "thumbnail": {
                            "url": "https://camo.githubusercontent.com/1a7eac730761ba836222ccdfd0bfa0e61e63ef34/68"
                                   "747470733a2f2f692e696d6775722e636f6d2f6b5962493948692e706e67"
                        },
                        "fields": [
                            {
                                "name": "Containers Monitored",
                                "value": f"{self.monitored_count}",
                                "inline": True
                            },
                            {
                                "name": "Containers Updated",
                                "value": f"{updated_count}",
                                "inline": True
                            }
                        ]
                    }
                ]
            }
            for container, old_image, new_image in container_tuples:
                json['embeds'][0]['fields'].append(
                    {
                        "name": container.name,
                        "value": 'Old SHA: {} | New SHA: {}'.format(
                            old_image.short_id.split(":")[1],
                            new_image.short_id.split(":")[1]
                        )
                    }
                )
            return json

    def post(self, json):
        """POST webhook for notifications"""
        for url in self.config.webhook_urls:
            try:
                headers = {'Content-Type': 'application/json', 'user-agent': 'ouroboros'}
                p = requests.post(url, json=json, headers=headers)
                self.logger.debug("Sent webhook successfully to %s | status code %s", url, p)
            except RequestException as e:
                self.logger.error("Error Posting to Webhook url %s | error %s", url, e)
