import requests

from logging import getLogger
from datetime import datetime, timezone
from requests.exceptions import RequestException


class NotificationManager(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager
        self.logger = getLogger()

    def send(self, container_tuples=None, socket=None, notification_type='data'):
        formatted_webhooks = []
        if self.config.webhook_urls:
            for webhook_url in self.config.webhook_urls:
                if notification_type == "keep_alive":
                    if "hc-ping" in webhook_url:
                        formatted_webhooks.append((webhook_url, {}))
                else:
                    if 'discord' in webhook_url:
                        format_type = 'discord'
                    elif 'slack' in webhook_url:
                        format_type = 'slack'
                    elif 'pushover' in webhook_url:
                        format_type = 'pushover'
                    elif 'hc-ping' in webhook_url:
                        continue
                    else:
                        format_type = 'default'

                    formatted_webhooks.append((webhook_url, self.format(container_tuples, socket, format_type)))

            self.post(formatted_webhooks)

    def format(self, container_tuples, socket, format_type):
        clean_socket = socket.split("//")[1]
        now = str(datetime.now(timezone.utc)).replace(" ", "T")
        if format_type in ['slack', 'default', 'pushover']:
            text = "Host Socket: {}\n".format(clean_socket)
            text += "Containers Monitored: {}\n".format(self.data_manager.monitored_containers[socket])
            text += "Containers Updated: {}\n".format(self.data_manager.total_updated[socket])
            for container, old_image, new_image in container_tuples:
                text += "{} updated from {} to {}\n".format(
                    container.name,
                    old_image.short_id.split(":")[1],
                    new_image.short_id.split(":")[1]
                )
            text += now
            if format_type == 'pushover':
                json = {
                    "html": 1,
                    "token": self.config.pushover_token,
                    "user": self.config.pushover_user,
                    "device": self.config.pushover_device,
                    "title": "Ouroboros updated containers:",
                    "message": text
                }
            else:
                json = {"text": text}
            return json

        elif format_type == 'discord':
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
                                "name": "Socket:",
                                "value": f"{clean_socket}"
                            },
                            {
                                "name": "Containers Monitored",
                                "value": f"{self.data_manager.monitored_containers[socket]}",
                                "inline": True
                            },
                            {
                                "name": "Containers Updated",
                                "value": f"{self.data_manager.total_updated[socket]}",
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

    def post(self, webhook_tuples):
        """POST webhook for notifications"""
        for url, json in webhook_tuples:
            try:
                headers = {'Content-Type': 'application/json', 'user-agent': 'ouroboros'}
                p = requests.post(url, json=json, headers=headers)
                self.logger.debug("Sent webhook successfully to %s | status code %s", url, p)
            except RequestException as e:
                self.logger.error("Error Posting to Webhook url %s | error %s", url, e)
