from time import sleep
from os import environ

from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ConnectionError
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

    core_group.add_argument('-t', '--docker-tls-verify', default=False, dest='DOCKER_TLS_VERIFY', action='store_true',
                            help='Enable docker TLS\n'
                                 'REQUIRES: docker cert mount')

    core_group.add_argument('-i', '--interval', type=int, default=Config.interval, dest='INTERVAL',
                            help='Interval in seconds between checking for updates\n'
                                 'DEFAULT: 300')

    core_group.add_argument('-C', '--cron', default=Config.cron, dest='CRON',
                            help='Cron formatted string for scheduling\n'
                                 'EXAMPLE: "*/5 * * * *"')

    core_group.add_argument('-l', '--log-level', choices=['debug', 'info', 'warn', 'error', 'critical'],
                            dest='LOG_LEVEL', default=Config.log_level, help='Set logging level\n'
                                                                             'DEFAULT: info')

    core_group.add_argument('-u', '--self-update', default=False, dest='SELF_UPDATE', action='store_true',
                            help='Let ouroboros update itself')

    core_group.add_argument('-o', '--run-once', default=False, action='store_true', dest='RUN_ONCE', help='Single run')

    core_group.add_argument('-A', '--dry-run', default=False, action='store_true', dest='DRY_RUN',
                            help='Run without making changes. Best used with run-once')

    core_group.add_argument('-N', '--notifiers', nargs='+', default=Config.notifiers, dest='NOTIFIERS',
                            help='Apprise formatted notifiers\n'
                                 'EXAMPLE: -N discord://1234123412341234/jasdfasdfasdfasddfasdf '
                                 'mailto://user:pass@gmail.com')

    docker_group = parser.add_argument_group("Docker", "Configuration of docker functionality")
    docker_group.add_argument('-m', '--monitor', nargs='+', default=Config.monitor, dest='MONITOR',
                              help='Which container(s) to monitor\n'
                                   'DEFAULT: All')

    docker_group.add_argument('-n', '--ignore', nargs='+', default=Config.ignore, dest='IGNORE',
                              help='Container(s) to ignore\n'
                                   'EXAMPLE: -n container1 container2')

    docker_group.add_argument('-k', '--label-enable', default=False, dest='LABEL_ENABLE', action='store_true',
                              help='Enable label monitoring for ouroboros label options\n'
                                   'Note: labels take precedence'
                                   'DEFAULT: False')

    docker_group.add_argument('-M', '--labels-only', default=False, dest='LABELS_ONLY', action='store_true',
                              help='Only watch containers that utilize labels\n'
                                   'This allows a more strict compliance for environments'
                                   'DEFAULT: False')

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
                            dest='PROMETHEUS_ADDR', help='Bind address to run Prometheus exporter on\n'
                                                         'DEFAULT: 127.0.0.1')

    data_group.add_argument('-p', '--prometheus-port', type=int, default=Config.prometheus_port,
                            dest='PROMETHEUS_PORT', help='Port to run Prometheus exporter on\n'
                                                         'DEFAULT: 8000')

    data_group.add_argument('-I', '--influx-url', default=Config.influx_url, dest='INFLUX_URL',
                            help='URL for influxdb\n'
                                  'DEFAULT: 127.0.0.1')

    data_group.add_argument('-P', '--influx-port', type=int, default=Config.influx_port, dest='INFLUX_PORT',
                            help='PORT for influxdb\n'
                                  'DEFAULT: 8086')

    data_group.add_argument('-U', '--influx-username', default=Config.influx_username, dest='INFLUX_USERNAME',
                            help='Username for influxdb\n'
                                  'DEFAULT: root')

    data_group.add_argument('-x', '--influx-password', default=Config.influx_password, dest='INFLUX_PASSWORD',
                            help='Password for influxdb\n'
                                  'DEFAULT: root')

    data_group.add_argument('-X', '--influx-database', default=Config.influx_password, dest='INFLUX_DATABASE',
                            help='Influx database name. Required if using influxdb')

    data_group.add_argument('-s', '--influx-ssl', default=False, dest='INFLUX_SSL', action='store_true',
                            help='Use SSL when connecting to influxdb')

    data_group.add_argument('-V', '--influx-verify-ssl', default=False, dest='INFLUX_VERIFY_SSL', action='store_true',
                            help='Verify SSL certificate when connecting to influxdb')

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
    scheduler = BackgroundScheduler()
    scheduler.start()

    for socket in config.docker_sockets:
        try:
            docker = Docker(socket, config, data_manager, notification_manager)
            if config.cron:
                scheduler.add_job(
                    docker.update_containers,
                    name=f'Cron container update for {socket}',
                    trigger='cron',
                    minute=config.cron[0],
                    hour=config.cron[1],
                    day=config.cron[2],
                    month=config.cron[3],
                    day_of_week=config.cron[4]
                )
            else:
                if config.run_once:
                    scheduler.add_job(docker.update_containers, name=f'Run Once container update for {socket}')
                else:
                    scheduler.add_job(
                        docker.update_containers,
                        name=f'Initial run interval container update for {socket}'
                    )
                    scheduler.add_job(
                        docker.update_containers,
                        name=f'Interval container update for {socket}',
                        trigger='interval', seconds=config.interval
                    )
        except ConnectionError:
            ol.logger.error("Could not connect to socket %s. Check your config", socket)

    if config.run_once:
        next_run = None
    elif config.cron:
        next_run = scheduler.get_jobs()[0].next_run_time
    else:
        now = datetime.now(timezone.utc).astimezone()
        next_run = (now + timedelta(0, config.interval)).strftime("%Y-%m-%d %H:%M:%S")

    notification_manager.send(kind='startup', next_run=next_run)

    while scheduler.get_jobs():
        sleep(1)

    scheduler.shutdown()


if __name__ == "__main__":
    main()
