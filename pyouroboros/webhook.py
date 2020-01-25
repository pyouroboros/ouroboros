from bottle import Bottle

from logging import getLogger
import threading


class HookManager(object):
    def __init__(self, config, modes, scheduler):
        self.config = config
        self.logger = getLogger()
        if not config.webhook:
            return
        self.modes = modes
        self.scheduler = scheduler

        self._app = Bottle()
        self._route()

        threading.Thread(target=self._app.run, kwargs=dict(host=self.config.webhook_addr, port=self.config.webhook_port), daemon=True).start()

    def _route(self):
        self._app.route('/update', method="POST", callback=self._index)

    def _index(self):
        for mode in self.modes:
            self.scheduler.add_job(mode.update, name=f'Webhook triggered update for {mode.socket}')
        return 'updated'

