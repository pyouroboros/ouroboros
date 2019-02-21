import apprise
from jinja2 import Environment, BaseLoader

from logging import getLogger
from datetime import datetime, timezone


class BaseMessage(object):
    def __init__(self, title, body):
        self.title = title
        self.body = body


class StartupMessage(BaseMessage):
    def __init__(self, hostname, next_run=None):
        now = datetime.now(timezone.utc).astimezone()
        title = f'Ouroboros has started'
        body_fields = [
            f'Host: {hostname}',
            f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")}',
            f'Next Run: {next_run}']
        super().__init__(title, '\n'.join(body_fields))


class TemplateMessage(BaseMessage):
    def __init__(self, title, config, socket, tuples, data_manager):
        template = Environment(loader=BaseLoader).from_string(config.template)
        body = template.render(
            socket=socket.split('//')[1],
            hostname=config.hostname,
            total_monitored=data_manager.monitored_containers[socket],
            total_updated=data_manager.total_updated[socket],
            updated_tuples=tuples
        )
        super().__init__(title, body)


class ContainerUpdateMessage(TemplateMessage):
    def __init__(self, config, socket, tuples, data_manager):
        title = f'Ouroboros has updated containers!'
        tuples = [(container,
                   old_image.short_id.split(':')[1],
                   new_image.short_id.split(':')[1])
                  for container, old_image, new_image in tuples]
        super().__init__(title, config, socket, tuples, data_manager)


class ServiceUpdateMessage(TemplateMessage):
    def __init__(self, config, socket, tuples, data_manager):
        title = f'Ouroboros has updated services!'
        super().__init__(title, config, socket, tuples, data_manager)


class NotificationManager(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager
        self.logger = getLogger()

        self.apprise = self.build_apprise(self.config.notifiers)

    def build_apprise(self, notifiers):
        asset = apprise.AppriseAsset(
            image_url_mask='https://bin.cajun.pro/images/ouroboros/notifications/ouroboros-logo-{XY}{EXTENSION}',
            default_extension='.png'
        )
        asset.app_id = "Ouroboros"
        asset.app_desc = "Ouroboros"
        asset.app_url = "https://github.com/pyouroboros/ouroboros"
        asset.html_notify_map['info'] = '#5F87C6'
        asset.image_url_logo = 'https://bin.cajun.pro/images/ouroboros/notifications/ouroboros-logo-256x256.png'

        apprise_obj = apprise.Apprise(asset=asset)

        for notifier in notifiers:
            if notifier:
                add = apprise_obj.add(notifier)
                if not add:
                    self.logger.error('Could not add notifier %s', notifier)

        return apprise_obj

    def send(self, message, notifiers=None):
        if notifiers:
            apprise = self.build_apprise(notifiers)
        else:
            apprise = self.apprise

        if apprise.servers:
            apprise.notify(title=message.title, body=message.body)
