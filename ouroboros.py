import schedule
from time import sleep
from os import environ

from argparse import ArgumentParser, RawTextHelpFormatter

from pyouroboros.config import Config
from pyouroboros.dockerclient import Docker
from pyouroboros.logger import OuroborosLogger


def main():
    """Declare command line options"""
    parser = ArgumentParser(description='ouroboros', formatter_class=RawTextHelpFormatter,
                            epilog='EXAMPLE: ouroboros -d tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn',)

    core_group = parser.add_argument_group("Core", "Configuration of core functionality")
    core_group.add_argument('-d', '--docker-socket', default=Config.docker_socket, dest='DOCKER_SOCKET',
                            help='Socket for docker management\n'
                                 'DEFAULT: "unix://var/run/docker.sock"')

    core_group.add_argument('-i', '--interval', type=int, default=Config.interval, dest='INTERVAL',
                            help='Interval in seconds between checking for updates\n'
                                 'DEFAULT: 300')

    core_group.add_argument('-l', '--loglevel', choices=['debug', 'info', 'warn', 'error', 'critical'],
                            dest='LOGLEVEL', default=Config.loglevel, help='Set logging level\n'
                                                                           'DEFAULT: info')

    core_group.add_argument('-o', '--runonce', default=False, action='store_true', dest='RUNONCE', help='Single run')

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
                              help='Private docker repository username\n'
                                   'EXAMPLE: foo@bar.baz')

    docker_group.add_argument('-R', '--repo-pass', default=None, dest='REPO_PASS',
                              help='Private docker repository password\n'
                                   'DEFAULT: 127.0.0.1')

    data_group = parser.add_argument_group('Data Export', 'Configuration of data export functionality')
    data_group.add_argument('-D', '--data-export', choices=['prometheus', 'influxdb'], default=None, dest='DATA_EXPORT',
                            help='Enable exporting of data for chosen option')

    data_group.add_argument('-a', '--prometheus-exporter-addr', default=Config.prometheus_exporter_addr,
                            dest='PROMETHEUS_EXPORTER_ADDR', help='Bind address to run Prometheus exporter on. '
                                                                  'Has no effect without --data-export prometheus\n'
                                                                  'DEFAULT: 127.0.0.1')

    data_group.add_argument('-p', '--prometheus-exporter-port', type=int, default=Config.prometheus_exporter_port,
                            dest='PROMETHEUS_EXPORTER_PORT', help='Port to run Prometheus exporter on. '
                                                                  'Has no effect without --data-export prometheus\n'
                                                                  'DEFAULT: 8000')

    data_group.add_argument('-w', '--webhook-urls', nargs='+', default=Config.webhook_urls, dest='WEBHOOK_URLS',
                            help='Webhook POST urls\n'
                                 'EXAMPLE: -w https://domain.tld/1234/asdf http://123.123.123.123:4040/re235')

    data_group.add_argument('-T', '--webhook-type', choices=['slack', 'discord'], default=Config.webhook_type,
                            dest='WEBHOOK_TYPE', help='Webhook POST urls\n'
                                                      'DEFAULT: slack')

    args = parser.parse_args()

    if environ.get('LOGLEVEL'):
        loglevel = environ.get('LOGLEVEL')
    else:
        loglevel = args.LOGLEVEL
    ol = OuroborosLogger(level=loglevel)
    ol.logger.info("pyouroboros configuration: %s", vars(args))
    config = Config(environment_vars=environ, cli_args=args)
    docker = Docker(config)

    if docker.monitored:
        schedule.every(config.interval).seconds.do(docker.update_containers).tag('update-containers')
    else:
        ol.logger.info('No containers are running or monitored')
        exit(1)

    schedule.run_all()

    if args.RUNONCE:
        schedule.clear('update-containers')

    while schedule.jobs:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
