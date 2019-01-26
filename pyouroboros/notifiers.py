import apprise

from logging import getLogger
from datetime import datetime, timezone


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

    def send(self, container_tuples=None, socket=None, kind='update'):
        if kind == 'startup':
            now = datetime.now(timezone.utc).astimezone()
            title = f'Ouroboros has started'
            body = f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")}'
        else:
            title = 'Ouroboros has updated containers!'
            body = f"Host Socket: {socket.split('//')[1]}\n"
            body += f"Containers Monitored: {self.data_manager.monitored_containers[socket]}\n"
            body += f"Total Containers Updated: {self.data_manager.total_updated[socket]}\n"
            body += f"Containers updated this pass: {len(container_tuples)}\n"
            for container, old_image, new_image in container_tuples:
                body += "{} updated from {} to {}\n".format(
                    container.name,
                    old_image.short_id.split(":")[1],
                    new_image.short_id.split(":")[1]
                )
        if self.apprise.servers:
            self.apprise.notify(title=title, body=body)
