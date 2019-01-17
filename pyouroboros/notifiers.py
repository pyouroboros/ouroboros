import requests

from email.message import EmailMessage
from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError, SMTPServerDisconnected, SMTPException
from logging import getLogger
from datetime import datetime, timezone
from requests.exceptions import RequestException

from pyouroboros.helpers import EMAIL_TEMPLATE


class NotificationManager(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager
        self.logger = getLogger()

        self.email = Email(self.config, self.data_manager)
        self.webhooks = Webhooks(self.config, self.data_manager)

    def send(self, container_tuples=None, socket=None, notification_type='data'):
        if self.email.server and notification_type == 'data':
            self.email.send(container_tuples, socket)

        if self.config.webhook_urls:
            self.webhooks.send(container_tuples, socket, notification_type)


class Email(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager

        self.logger = getLogger()
        if self.config.smtp_host:
            self.server = True
        else:
            self.server = False

    def get_server(self):
        try:
            server = SMTP(
                host=self.config.smtp_host,
                port=self.config.smtp_port
            )
            if self.config.smtp_starttls:
                server.starttls()
            if self.config.smtp_username and self.config.smtp_password:
                server.login(self.config.smtp_username, self.config.smtp_password)
            return server
        except SMTPConnectError as e:
            self.logger.error('Could not connect to SMTP host %s on port %s. Disabling SMTP. Error: %s',
                              self.config.smtp_host, self.config.smtp_port, e)
            return
        except SMTPAuthenticationError as e:
            self.logger.error('SMTP host did not accept credentials. Disabling SMTP. Error %s', e)
            return

    def send(self, container_tuples, socket):
        for address in self.config.smtp_recipients:
            msg = EmailMessage()
            msg['Subject'] = 'Ouroboros has updated containers!'
            msg['From'] = f"{self.config.smtp_from_name} <{self.config.smtp_from_email}>"
            msg['To'] = address

            container_updates = ''
            for container, old_image, new_image in container_tuples:
                container_updates += "{} updated from {} to {}\n".format(
                    container.name,
                    old_image.short_id.split(":")[1],
                    new_image.short_id.split(":")[1]
                )

            template = EMAIL_TEMPLATE.substitute(
                CONTAINERS_MONITORED=self.data_manager.monitored_containers[socket],
                CONTAINERS_UPDATED=self.data_manager.total_updated[socket],
                HOST_SOCKET=socket.split("//")[1],
                CONTAINER_UPDATES=container_updates)

            msg.set_content(template)
            try:
                server = self.get_server()
                server.send_message(msg)
            except SMTPServerDisconnected as e:
                self.server = False
                self.logger.error('Could not properly talk to SMTP server. Disabling SMTP. Error: %s', e)
            except SMTPException as e:
                self.server = False
                self.logger.error('SMTP Error: %s', e)


class Webhooks(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager

        self.logger = getLogger()

    def send(self, container_tuples, socket, notification_type):
        formatted_webhooks = []
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
                    "title": "Ouroboros has updated containers!",
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
                            "url": "https://bin.cajun.pro/images/ouroboros/ouroboros_logo_primary_cropped.png"
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
