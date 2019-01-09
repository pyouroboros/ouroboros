#!/usr/bin/env python3
from time import sleep
from os import environ
from Ouroboros.logger import set_logger
from Ouroboros.dockerclient import Docker
from argparse import ArgumentParser, RawTextHelpFormatter

import schedule
import logging
from Ouroboros.config import Config


def main():

    config = Config(environ, args)
    docker = Docker(config)

    if docker.monitored:
        schedule.every(config.interval).seconds.do(docker.update_containers).tag('update-containers')
    else:
        log.info('No containers are running or monitored')
        exit(1)
    # log.info(f"Ouroboros configuration: {vars(args)}")

    schedule.run_all()

    if args.run_once:
        schedule.clear('update-containers')

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    """Declare command line options"""
    parser = ArgumentParser(description='ouroboros', formatter_class=RawTextHelpFormatter,
                            epilog='EXAMPLE: ouroboros -d tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn',)

    parser.add_argument('-d', '--docker-socket', default=Config.docker_socket, dest='DOCKER_SOCKET',
                        help='Socket for docker management\n'
                             'DEFAULT: "unix://var/run/docker.sock"')

    parser.add_argument('-i', '--interval', type=int, default=Config.interval, dest='INTERVAL',
                        help='Interval in seconds between checking for updates\n'
                             'DEFAULT: 300')

    parser.add_argument('-m', '--monitor', nargs='+', default=Config.monitor, dest='MONITOR',
                        help='Which container(s) to monitor\n'
                             'DEFAULT: All')

    parser.add_argument('-n', '--ignore', nargs='+', default=Config.ignore, dest='IGNORE',
                        help='Container(s) to ignore\n'
                             'EXAMPLE: -n container1 container2')

    parser.add_argument('-l', '--loglevel', choices=['debug', 'info', 'warn', 'error', 'critical'],
                        dest='LOGLEVEL', default=Config.loglevel, help='Set logging level\n'
                                                                       'DEFAULT: info')

    parser.add_argument('-o', '--runonce', default=False, type=bool, action='store_true', dest='RUNONCE',
                        help='Single run')

    parser.add_argument('-c', '--cleanup', default=False, dest='CLEANUP', action='store_true', type=bool,
                        help='Remove old images after updating')

    parser.add_argument('-L', '--latest', default=False, dest='LATEST', type=bool, action='store_true',
                        help='Check for latest image instead of pulling current tag')

    parser.add_argument('-P', '--prometheus', default=False, dest='PROMETHEUS', type=bool, action='store_true',
                        help='Enable Prometheus exporter')

    parser.add_argument('-a', '--prometheus-exporter-addr', default=Config.prometheus_exporter_addr,
                        dest='PROMETHEUS_EXPORTER_ADDR', help='Bind address to run Prometheus exporter on\n'
                                                              'DEFAULT: 127.0.0.1')

    parser.add_argument('-p', '--prometheus-exporter-port', type=int, default=Config.prometheus_exporter_port,
                        dest='PROMETHEUS_EXPORTER_PORT', help='Port to run Prometheus exporter on\n'
                                                              'DEFAULT: 8000')

    parser.add_argument('-w', '--webhook-urls', nargs='+', default=Config.webhook_urls, dest='WEBHOOK_URLS',
                        help='Webhook POST urls\n'
                             'EXAMPLE: -w https://domain.tld/1234/asdf http://123.123.123.123:4040/re235')

    parser.add_argument('-r', '--repo-user', default=Config.prometheus_exporter_addr, dest='REPO_USER',
                        help='Private docker repository username\n'
                              'EXAMPLE: foo@bar.baz')

    parser.add_argument('-R', '--repo-pass', default=Config.prometheus_exporter_addr, dest='REPO_PASS',
                        help='Private docker repository password\n'
                              'DEFAULT: 127.0.0.1')

    args = parser.parse_args()

    log = logging.getLogger()

    main()
