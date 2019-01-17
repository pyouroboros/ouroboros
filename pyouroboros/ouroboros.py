import schedule
from time import sleep
from os import environ

from argparse import ArgumentParser, RawTextHelpFormatter

from pyouroboros.config import Config
from pyouroboros.dockerclient import Docker
from pyouroboros.logger import OuroborosLogger
from pyouroboros.dataexporters import DataManager
from pyouroboros.notifiers import NotificationManager
from pyouroboros import VERSION, BRANCH


def main():
    """Declare command line options"""
    parser = ArgumentParser(description='ouroboros', formatter_class=RawTextHelpFormatter,
                            epilog='EXAMPLE: ouroboros -d tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn')

    core_group = parser.add_argument_group("Core", "Configuration of core functionality")
    core_group.add_argument('-v', '--version', action='version', version=VERSION)

    core_group.add_argument('-d', '--docker-sockets', nargs='+', default=Config.docker_sockets, dest='DOCKER_SOCKETS',
                            help='Sockets for docker management\n'
                                 'DEFAULT: "unix://var/run/docker.sock"\n'
                                 'EXAMPLE: -d unix://var/run/docker.sock tcp://192.168.1.100:2376')

    core_group.add_argument('-i', '--interval', type=int, default=Config.interval, dest='INTERVAL',
                            help='Interval in seconds between checking for updates\n'
                                 'DEFAULT: 300')

    core_group.add_argument('-l', '--log-level', choices=['debug', 'info', 'warn', 'error', 'critical'],
                            dest='LOG_LEVEL', default=Config.log_level, help='Set logging level\n'
                                                                             'DEFAULT: info')

    core_group.add_argument('-u', '--self-update', default=False, dest='SELF_UPDATE', action='store_true',
                            help='Let ouroboros update itself')

    core_group.add_argument('-o', '--run-once', default=False, action='store_true', dest='RUN_ONCE', help='Single run')

    docker_group = parser.add_argument_group("Docker", "Configuration of docker functionality")
    docker_group.add_argument('-m', '--monitor', nargs='+', default=Config.monitor, dest='MONITOR',
                              help='Which container(s) to monitor\n'
                                   'DEFAULT: All')

    docker_group.add_argument('-n', '--ignore', nargs='+', default=Config.ignore, dest='IGNORE',
                              help='Container(s) to ignore\n'
                                   'EXAMPLE: -n container1 container2')

    docker_group.add_argument('-c', '--cleanup', default=False, dest='CLEANUP', action='store_true',
                              help='Remove old images after updating')

    docker_group.add_argument('-L', '--latest', default=False, dest='LATEST', action='store_true',
                              help='Check for latest image instead of pulling current tag')

    docker_group.add_argument('-r', '--repo-user', default=None, dest='REPO_USER',
                              help='Private docker registry username\n'
                                   'EXAMPLE: foo@bar.baz')

    docker_group.add_argument('-R', '--repo-pass', default=None, dest='REPO_PASS',
                              help='Private docker registry password\n'
                                   'EXAMPLE: MyPa$$w0rd')

    data_group = parser.add_argument_group('Data Export', 'Configuration of data export functionality')
    data_group.add_argument('-D', '--data-export', choices=['prometheus', 'influxdb'], default=None, dest='DATA_EXPORT',
                            help='Enable exporting of data for chosen option')

    data_group.add_argument('-a', '--prometheus-addr', default=Config.prometheus_addr,
                            dest='PROMETHEUS_ADDR', help='Bind address to run Prometheus exporter on. '
                                                         'Has no effect without --data-export prometheus\n'
                                                         'DEFAULT: 127.0.0.1')

    data_group.add_argument('-p', '--prometheus-port', type=int, default=Config.prometheus_port,
                            dest='PROMETHEUS_PORT', help='Port to run Prometheus exporter on. '
                                                         'Has no effect without --data-export prometheus\n'
                                                         'DEFAULT: 8000')

    data_group.add_argument('-I', '--influx-url', default=Config.influx_url, dest='INFLUX_URL',
                            help='URL for influxdb, Has no effect without --data-export influxdb\n'
                                  'DEFAULT: 127.0.0.1')

    data_group.add_argument('-P', '--influx-port', type=int, default=Config.influx_port, dest='INFLUX_PORT',
                            help='PORT for influxdb, Has no effect without --data-export influxdb\n'
                                  'DEFAULT: 8086')

    data_group.add_argument('-U', '--influx-username', default=Config.influx_username, dest='INFLUX_USERNAME',
                            help='Username for influxdb, Has no effect without --data-export influxdb\n'
                                  'DEFAULT: root')

    data_group.add_argument('-x', '--influx-password', default=Config.influx_password, dest='INFLUX_PASSWORD',
                            help='Password for influxdb, Has no effect without --data-export influxdb\n'
                                  'DEFAULT: root')

    data_group.add_argument('-X', '--influx-database', default=Config.influx_password, dest='INFLUX_DATABASE',
                            help='Database for influxdb, Required if using influxdb. Has no effect without '
                                 '--data-export influxdb.\n'
                                  'DEFAULT: root')

    data_group.add_argument('-s', '--influx-ssl', default=False, dest='INFLUX_SSL', action='store_true',
                            help='Use SSL when connecting to influxdb')

    data_group.add_argument('-V', '--influx-verify-ssl', default=False, dest='INFLUX_VERIFY_SSL', action='store_true',
                            help='Verify SSL certificate when connecting to influxdb')

    notification_group = parser.add_argument_group('Notifications', 'Configuration of notification functionality')
    notification_group.add_argument('-w', '--webhook-urls', nargs='+', default=Config.webhook_urls, dest='WEBHOOK_URLS',
                                    help='Webhook POST urls\n'
                                         'EXAMPLE: -w https://domain.tld/1234/asdf http://123.123.123.123:4040/re235')

    notification_group.add_argument('-y', '--pushover-token', default=Config.pushover_token, dest='PUSHOVER_TOKEN',
                                    help='Pushover token to authenticate against application\n'
                                         'EXAMPLE: -y af2r52352asd')

    notification_group.add_argument('-Y', '--pushover-device', default=Config.pushover_device, dest='PUSHOVER_DEVICE',
                                    help='Device to receive pushover notification\n'
                                         'EXAMPLE: -Y SamsungGalaxyS8')

    notification_group.add_argument('-z', '--pushover-user', default=Config.pushover_user, dest='PUSHOVER_USER',
                                    help='Pushover user bound to application\n'
                                         'EXAMPLE: -z asdfweawefasdfawef')

    notification_group.add_argument('-e', '--smtp-host', default=Config.smtp_host, dest='SMTP_HOST',
                                    help='SMTP relay hostname\n'
                                         'EXAMPLE: -e smtp.gmail.com')

    notification_group.add_argument('-E', '--smtp-port', default=Config.smtp_port, type=int, dest='SMTP_PORT',
                                    help='SMTP relay port\n'
                                         'EXAMPLE: -E 587')

    notification_group.add_argument('-f', '--smtp-starttls', default=False, dest='SMTP_STARTTLS', action='store_true',
                                    help='SMTP relay uses STARTTLS')

    notification_group.add_argument('-F', '--smtp-username', default=Config.smtp_username, dest='SMTP_USERNAME',
                                    help='SMTP relay username\n'
                                         'EXAMPLE: -F ouroboros@ouroboros.com')

    notification_group.add_argument('-g', '--smtp-password', default=Config.smtp_password, dest='SMTP_PASSWORD',
                                    help='SMTP relay password\n'
                                         'EXAMPLE: -g MyPa$$w0rd')

    notification_group.add_argument('-G', '--smtp-recipients', default=Config.smtp_recipients, dest='SMTP_RECIPIENTS',
                                    nargs='+', help='SMTP notification recipients\n'
                                                    'EXAMPLE: -G ouroboros@ouroboros.com ouroboros2@ouroboros.com')

    notification_group.add_argument('-j', '--smtp-from-email', default=Config.smtp_from_email, dest='SMTP_FROM_EMAIL',
                                    help='SMTP from email\n'
                                         'EXAMPLE: -g notifications@ouroboros.com')

    notification_group.add_argument('-J', '--smtp-from-name', default=Config.smtp_from_name, dest='SMTP_FROM_NAME',
                                    help='SMTP from name\n'
                                         'DEFAULT: Ouroboros')

    args = parser.parse_args()

    if environ.get('LOG_LEVEL'):
        log_level = environ.get('LOG_LEVEL')
    else:
        log_level = args.LOG_LEVEL
    ol = OuroborosLogger(level=log_level)
    ol.logger.info('Version: %s-%s', VERSION, BRANCH)
    config = Config(environment_vars=environ, cli_args=args)
    config_dict = {key: value for key, value in vars(config).items() if key.upper() in config.options}
    ol.logger.debug("Ouroboros configuration: %s", config_dict)

    data_manager = DataManager(config)
    notification_manager = NotificationManager(config, data_manager)

    for socket in config.docker_sockets:
        docker = Docker(socket, config, data_manager, notification_manager)
        schedule.every(config.interval).seconds.do(docker.update_containers).tag(f'update-containers-{socket}')

    schedule.run_all()

    if args.RUN_ONCE:
        for socket in config.docker_sockets:
            schedule.clear(f'update-containers-{socket}')

    while schedule.jobs:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
