import apprise

from logging import getLogger
from datetime import datetime, timezone


class BaseMessage(object):
    def __init__(self, title, body_fields):
        self.title = title
        self.body_fields = body_fields

    @property
    def body(self):
        return '\r\n'.join(self.body_fields)


class StartupMessage(BaseMessage):
    def __init__(self, hostname, next_run=None):
        now = datetime.now(timezone.utc).astimezone()
        title = f'Ouroboros has started'
        body_fields = [
            f'Host: {hostname}',
            f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")}',
            f'Next Run: {next_run}']
        super().__init__(title, body_fields)


class ContainerUpdateMessage(BaseMessage):
    def __init__(self, config, socket, container_tuples, data_manager):
        title = f'Ouroboros has updated containers!'
        body_fields = []
        if not config.notifier_short_message:
            body_fields.extend(
                [
                    f"Host/Socket: {config.hostname} / {socket.split('//')[1]}",
                    f"Containers Monitored: {data_manager.monitored_containers[socket]}",
                    f"Total Containers Updated: {data_manager.total_updated[socket]}",
                    f"Containers updated this pass: {len(container_tuples)}"
                ]
            )
        body_fields.extend(
            [
                "{} updated from {} to {}".format(
                    container.name,
                    old_image.short_id.split(':')[1],
                    new_image.short_id.split(':')[1]
                ) for container, old_image, new_image in container_tuples
            ]
        )
        super().__init__(title, body_fields)


class ServiceUpdateMessage(BaseMessage):
    def __init__(self, config, socket, service_tuples, data_manager):
        title = f'Ouroboros has updated services!'
        body_fields = []
        if not config.notifier_short_message:
            body_fields.extend(
                [
                    f"Host/Socket: {config.hostname}",
                    f"Services Monitored: {data_manager.monitored_containers[socket]}",
                    f"Total services Updated: {data_manager.total_updated[socket]}",
                    f"Services updated this pass: {len(service_tuples)}"
                ]
            )
        body_fields.extend(
            [
                "{} updated from {} to {}".format(
                    service.name,
                    old_image_sha,
                    new_image_sha
                ) for service, old_image_sha, new_image_sha in service_tuples
            ]
        )
        super().__init__(title, body_fields)


class NotificationManager(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager
        self.logger = getLogger()

        self.apprise = self.build_apprise()

    def build_apprise(self):
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

        for notifier in self.config.notifiers:
            add = apprise_obj.add(notifier)
            if not add:
                self.logger.error('Could not add notifier %s', notifier)

        return apprise_obj

    def send(self, message):
        if self.apprise.servers:
            self.apprise.notify(title=message.title, body=message.body)
