import argparse
import docker
import re
import defaults

host = ''
interval = ''
monitor = []
level = ''
api_client = None

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

def parser(sysargs):
    """Declare command line options"""
    global host, interval, monitor, level, api_client
    parser = argparse.ArgumentParser(description='ouroboros', epilog='Example: python3 main.py -u tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn')
    parser.add_argument('-u', '--url', help='Url for tcp host (defaults to "unix://var/run/docker.sock")', required=False)
    parser.add_argument('-i', '--interval', type=int, help='Interval in seconds between checking for updates (defaults to 300s)', required=False)
    parser.add_argument('-m', '--monitor', nargs='+', help='Which container to monitor (defaults to all running).', required=False)
    parser.add_argument('-l', '--loglevel', choices=['notset', 'debug', 'info', 'warn', 'error', 'critical'], help='Change logger mode (defaults to info)', required=False)
    args = parser.parse_args(sysargs)
    if args.url:
        host = args.url
        if not checkURI(host):
            host = defaults.LOCAL_UNIX_SOCKET
    interval = args.interval or defaults.INTERVAL
    monitor = args.monitor or []
    level = args.loglevel or 'info'
    api_client = docker.APIClient(base_url=host)
    return args
