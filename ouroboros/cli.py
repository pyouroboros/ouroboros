from os import environ
import argparse
import docker
import re
import defaults

host = ''
interval = ''
monitor = []
loglevel = ''
api_client = None
run_once = None
cleanup = None

def checkURI(uri):
    """Validate tcp:// regex"""
    regex = re.compile(
        r'^(?:tcp)s?://' # tcp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, uri)


def get_interval_env():
    """Attempt to convert INTERVAL environment variable to int"""
    int_env = environ.get('INTERVAL')
    try:
        return int(int_env)
    except:
        return False


def parser(sysargs):
    """Declare command line options"""
    global host, interval, monitor, loglevel, api_client, run_once, cleanup
    parser = argparse.ArgumentParser(description='ouroboros',
                                     epilog='Example: python3 main.py -u tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn')
    parser.add_argument('-u', '--url', help='Url for tcp host (defaults to "unix://var/run/docker.sock")')
    parser.add_argument('-i', '--interval', type=int, default=get_interval_env() or defaults.INTERVAL,
                        help='Interval in seconds between checking for updates (defaults to 300s)')
    parser.add_argument('-m', '--monitor', nargs='+', default=environ.get('MONITOR') or [],
                        help='Which container to monitor (defaults to all running).')
    parser.add_argument('-l', '--loglevel', choices=['notset', 'debug', 'info', 'warn', 'error', 'critical'],
                        default=environ.get('LOGLEVEL') or 'info', help='Change logger mode (defaults to info)')
    parser.add_argument('-r', '--runonce', default=environ.get('RUNONCE') or False,
                        help='Only run ouroboros once then exit', action='store_true')
    parser.add_argument('-c', '--cleanup', default=environ.get('CLEANUP') or False,
                        help='Remove old images after updating', action='store_true')
    args = parser.parse_args(sysargs)

    if args.url:
        host = args.url
        if not checkURI(host):
            host = defaults.LOCAL_UNIX_SOCKET

    interval = args.interval
    monitor = args.monitor
    loglevel = args.loglevel
    run_once = args.runonce
    cleanup = args.cleanup
    api_client = docker.APIClient(base_url=host)
    return args
