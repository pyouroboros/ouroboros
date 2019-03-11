from os import environ
from logging import getLogger
from pyouroboros.logger import BlacklistFilter


class Config(object):
    options = ['INTERVAL', 'PROMETHEUS', 'DOCKER_SOCKETS', 'MONITOR', 'IGNORE', 'LOG_LEVEL', 'PROMETHEUS_ADDR',
               'PROMETHEUS_PORT', 'NOTIFIERS', 'REPO_USER', 'REPO_PASS', 'CLEANUP', 'RUN_ONCE', 'CRON',
               'INFLUX_URL', 'INFLUX_PORT', 'INFLUX_USERNAME', 'INFLUX_PASSWORD', 'INFLUX_DATABASE', 'INFLUX_SSL',
               'INFLUX_VERIFY_SSL', 'DATA_EXPORT', 'SELF_UPDATE', 'LABEL_ENABLE', 'DOCKER_TLS', 'LABELS_ONLY',
               'DRY_RUN', 'HOSTNAME', 'DOCKER_TLS_VERIFY', 'SWARM', 'SKIP_STARTUP_NOTIFICATIONS']

    hostname = environ.get('HOSTNAME')
    interval = 300
    cron = None
    docker_sockets = 'unix://var/run/docker.sock'
    docker_tls = False
    docker_tls_verify = True
    swarm = False
    monitor = []
    ignore = []
    data_export = None
    log_level = 'info'
    cleanup = False
    run_once = False
    dry_run = False
    self_update = False
    label_enable = False
    labels_only = False

    repo_user = None
    repo_pass = None
    auth_json = None

    prometheus = False
    prometheus_addr = '127.0.0.1'
    prometheus_port = 8000

    influx_url = '127.0.0.1'
    influx_port = 8086
    influx_ssl = False
    influx_verify_ssl = False
    influx_username = 'root'
    influx_password = 'root'
    influx_database = None

    notifiers = []
    skip_startup_notifications = False

    def __init__(self, environment_vars, cli_args):
        self.cli_args = cli_args
        self.environment_vars = environment_vars
        self.filtered_strings = None

        self.logger = getLogger()
        self.parse()

    def config_blacklist(self):
        filtered_strings = [getattr(self, key.lower()) for key in Config.options
                            if key.lower() in BlacklistFilter.blacklisted_keys]
        # Clear None values
        self.filtered_strings = list(filter(None, filtered_strings))
        # take lists inside of list and append to list
        for index, value in enumerate(self.filtered_strings, 0):
            if isinstance(value, list):
                self.filtered_strings.extend(self.filtered_strings.pop(index))
                self.filtered_strings.insert(index, self.filtered_strings[-1:][0])
        # Added matching for ports
        ports = [string.split(':')[0] for string in self.filtered_strings if ':' in string]
        self.filtered_strings.extend(ports)
        # Added matching for tcp sockets. ConnectionPool ignores the tcp://
        tcp_sockets = [string.split('//')[1] for string in self.filtered_strings if '//' in string]
        self.filtered_strings.extend(tcp_sockets)
        # Get JUST hostname from tcp//unix
        for socket in getattr(self, 'docker_sockets'):
            self.filtered_strings.append(socket.split('//')[1].split(':')[0])

        for handler in self.logger.handlers:
            handler.addFilter(BlacklistFilter(set(self.filtered_strings)))

    def parse(self):
        for option in Config.options:
            if self.environment_vars.get(option):
                env_opt = self.environment_vars[option]
                if isinstance(env_opt, str):
                    # Clean out quotes, both single/double and whitespace
                    env_opt = env_opt.strip("'").strip('"').strip(' ')
                if option in ['INTERVAL', 'PROMETHEUS_PORT', 'INFLUX_PORT']:
                    try:
                        opt = int(env_opt)
                        setattr(self, option.lower(), opt)
                    except ValueError as e:
                        print(e)
                elif option in ['CLEANUP', 'RUN_ONCE', 'INFLUX_SSL', 'INFLUX_VERIFY_SSL', 'DRY_RUN', 'SWARM',
                                'SELF_UPDATE', 'LABEL_ENABLE', 'DOCKER_TLS', 'LABELS_ONLY', 'DOCKER_TLS_VERIFY',
                                'SKIP_STARTUP_NOTIFICATIONS']:
                    if env_opt.lower() in ['true', 'yes']:
                        setattr(self, option.lower(), True)
                    elif env_opt.lower() in ['false', 'no']:
                        setattr(self, option.lower(), False)
                    else:
                        self.logger.error('%s is not true/yes, nor false/no for %s. Assuming %s',
                                          env_opt, option, getattr(self, option))
                else:
                    setattr(self, option.lower(), env_opt)
            elif vars(self.cli_args).get(option):
                setattr(self, option.lower(), vars(self.cli_args).get(option))

        # Specific var changes
        if self.repo_user and self.repo_pass:
            self.auth_json = {'Username': self.repo_user, 'Password': self.repo_pass}

        if self.interval < 30:
            self.interval = 30

        if self.labels_only and not self.label_enable:
            self.logger.warning('labels_only enabled but not in use without label_enable')

        for option in ['docker_sockets', 'notifiers', 'monitor', 'ignore']:
            if isinstance(getattr(self, option), str):
                string_list = getattr(self, option)
                setattr(self, option, [string for string in string_list.split(' ')])

        # Config sanity checks
        if self.cron:
            cron_times = self.cron.strip().split(' ')
            if len(cron_times) != 5:
                self.logger.error("Cron must be in cron syntax. e.g. * * * * * (5 places). Ignoring and using interval")
                self.cron = None
            else:
                self.logger.info("Cron configuration is valid. Using Cron schedule %s", cron_times)
                self.cron = cron_times
                self.interval = None

        if self.data_export == 'influxdb' and not self.influx_database:
            self.logger.error("You need to specify an influx database if you want to export to influxdb. Disabling "
                              "influxdb data export.")

        if self.data_export == 'prometheus' and self.self_update:
            self.logger.warning("If you bind a port to ouroboros, it will be lost when it updates itself.")

        if self.dry_run and not self.run_once:
            self.logger.warning("Dry run is designed to be ran with run once. Setting for you.")
            self.run_once = True

        # Remove default config that is not used for cleaner logs
        if self.data_export != 'prometheus':
            self.prometheus_addr, self.prometheus_port = None, None

        if self.data_export != 'influxdb':
            self.influx_url, self.influx_port, self.influx_username, self.influx_password = None, None, None, None

        self.config_blacklist()
