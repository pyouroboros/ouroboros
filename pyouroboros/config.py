from logging import getLogger

from pyouroboros.logger import BlacklistFilter


class Config(object):
    options = ['INTERVAL', 'PROMETHEUS', 'DOCKER_SOCKET', 'MONITOR', 'IGNORE', 'LOGLEVEL', 'PROMETHEUS_EXPORTER_ADDR'
               'PROMETHEUS_EXPORTER_PORT', 'WEBHOOK_URLS', 'REPO_USER', 'REPO_PASS', 'CLEANUP', 'RUNONCE', 'LATEST',
               'WEBHOOK_TYPE']

    interval = 300
    docker_socket = 'unix://var/run/docker.sock'
    monitor = []
    ignore = []
    webhook_urls = []
    webhook_type = 'slack'
    data_export = None
    log_level = 'info'
    latest = False
    cleanup = False
    run_once = False

    repo_user = None
    repo_pass = None
    auth_json = None

    prometheus = False
    prometheus_exporter_addr = '127.0.0.1'
    prometheus_exporter_port = 8000

    influx_url = '127.0.0.1'
    influx_port = 8086
    influx_username = 'root'
    influx_password = 'root'
    influx_database = None

    def __init__(self, environment_vars, cli_args):
        self.cli_args = cli_args
        self.environment_vars = environment_vars
        self.filtered_strings = None

        self.logger = getLogger()
        self.parse()

    def config_blacklist(self):
        filtered_strings = [getattr(self, value.lower()) for value in Config.options
                            if value in BlacklistFilter.blacklisted_strings]
        self.filtered_strings = list(filter(None, filtered_strings))
        # Added matching for domains that use /locations. ConnectionPool ignores the location in logs
        domains_only = [string.split('/')[0] for string in filtered_strings if '/' in string]
        self.filtered_strings.extend(domains_only)
        # Added matching for domains that use :port. ConnectionPool splits the domain/ip from the port
        without_port = [string.split(':')[0] for string in filtered_strings if ':' in string]
        self.filtered_strings.extend(without_port)

        for handler in self.logger.handlers:
            handler.addFilter(BlacklistFilter(set(self.filtered_strings)))

    def parse(self):
        for option in Config.options:
            if self.environment_vars.get(option):
                if option == 'INTERVAL' or option == 'PROMETHEUS_EXPORTER_PORT':
                    try:
                        opt = int(self.environment_vars[option])
                        setattr(self, option, opt)
                    except ValueError as e:
                        print(e)
                else:
                    setattr(self, option, self.environment_vars[option])
            elif vars(self.cli_args).get(option):
                setattr(self, option.lower(), vars(self.cli_args).get(option))

        if self.repo_user and self.repo_pass:
            self.auth_json = {'username': self.repo_user, 'password': self.repo_pass}

        if self.interval < 30:
            self.interval = 30
