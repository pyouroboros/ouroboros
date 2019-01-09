import prometheus_client

from Ouroboros.helpers import checkuri


class Config(object):
    options = ['INTERVAL', 'PROMETHEUS', 'DOCKER_SOCKET', 'MONITOR', 'IGNORE', 'LOGLEVEL', 'PROMETHEUS_EXPORTER_ADDR'
               'PROMETHEUS_EXPORTER_PORT', 'WEBHOOK_URLS', 'REPO_USER', 'REPO_PASS', 'CLEANUP', 'RUNONCE', 'KEEP_TAG']

    interval = 300
    docker_socket = 'unix://var/run/docker.sock'
    monitor = []
    ignore = []
    webhook_urls = []

    loglevel = 'info'
    keep_tag = False
    cleanup = False
    runonce = False

    repo_user = None
    repo_pass = None
    auth_json = None

    prometheus = False
    prometheus_exporter_addr = '127.0.0.1'
    prometheus_exporter_port = 8000

    def __init__(self, environment_vars, cli_args):
        self.cli_args = cli_args
        self.environment_vars = environment_vars

        self.parse()
        self.initialize()

    def parse(self):
        for option in Config.options:
            if self.environment_vars[option]:
                if option == 'INTERVAL' or option == 'PROMETHEUS_EXPORTER_PORT':
                    try:
                        opt = int(self.environment_vars[option])
                        setattr(self, option, opt)
                    except ValueError as e:
                        print(e)
                else:
                    setattr(self, option, self.environment_vars[option])
            elif self.cli_args[option]:
                setattr(self, option, self.cli_args[option])
        if not checkuri(self.docker_socket):
            self.docker_socket = Config.docker_socket

        if self.repo_user and self.repo_pass:
            self.auth_json = {'username': self.repo_user, 'password': self.repo_pass}

    def initialize(self):
        if self.prometheus:
            prometheus_client.start_http_server(self.prometheus_exporter_port, addr=self.prometheus_exporter_addr)
