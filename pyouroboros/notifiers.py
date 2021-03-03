import apprise
import gettext

from logging import getLogger
from datetime import datetime, timezone


class NotificationManager(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager
        self.logger = getLogger()

        self.apprise = self.build_apprise()
        self._ = None

        try:
            language = gettext.translation('notifiers', localedir='locales', languages=self.config.language)
            language.install()
            self._ = language.gettext
        except FileNotFoundError:
            self.logger.error("Can't find the '%s' language", self.config.language)
            self._ = gettext.gettext

    def build_apprise(self):
        asset = apprise.AppriseAsset(
            image_url_mask='https://i.imgur.com/L40ksWY.png',
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
                self.logger.error(_('Could not add notifier %s'), notifier)

        return apprise_obj

    def send(self, container_tuples=None, socket=None, kind='update', next_run=None, mode='container'):
        if kind == 'startup':
            now = datetime.now(timezone.utc).astimezone()            
            title = _('Ouroboros has started')
            body_fields = [
                _('Host: %s') % self.config.hostname,
                _('Time: %s') % now.strftime(_("%Y-%m-%d %H:%M:%S")),
                _('Next Run: %s') % next_run]
        else:
            title = _('Ouroboros has updated containers!')
            body_fields = [
                _('Host/Socket: %s / %s') % (self.config.hostname, socket.split('//')[1]),
                _('Containers Monitored: %d') % self.data_manager.monitored_containers[socket],
                _('Total Containers Updated: %d') % self.data_manager.total_updated[socket],
                _('Containers updated this pass: %d') % len(container_tuples)
            ]
            body_fields.extend(
                [
                    _("{} updated from {} to {}").format(
                        container.name,
                        old_image if mode == 'service' else old_image.short_id.split(':')[1],
                        new_image.short_id.split(':')[1]
                    ) for container, old_image, new_image in container_tuples
                ]
            )
        body = '\r\n'.join(body_fields)

        if self.apprise.servers:
            self.apprise.notify(title=title, body=body)
