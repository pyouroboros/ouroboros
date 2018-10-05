import defaults
import argparse
import docker
import re

host = ''
interval = ''
monitor = []
debug = ''
api_client = None

def checkURI(uri):
    regex = re.compile(
        r'^(?:unix|http|https)s?://' # unix:// or http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, uri) is None:
        exit('--socket value error: {} is not a valid URI'.format(uri))

def parser():
    global host, interval, monitor, debug, api_client
    parser = argparse.ArgumentParser(description='ouroboros', epilog='Example: python3 main.py -u tcp://1.2.3.4:5678 -i 20 -m container1 container2 -d warn')
    parser.add_argument('-u', '--url', help='Url for tcp host (defaults to "unix://var/run/docker.sock")', required=False)
    parser.add_argument('-i','--interval', type=int, help='Interval in seconds between checking for updates (defaults to 300s)', required=False)
    parser.add_argument('-m','--monitor', nargs='+', help='Which container to monitor (defaults to all found).', required=False)
    parser.add_argument('-d','--debug', choices=['notset','debug','info', 'warn', 'error', 'critical'], help='Change logger mode to debug (defaults to warn)', required=False)
    args = parser.parse_args()
    host = args.url or defaults.LOCAL_UNIX_SOCKET
    # checkURI(host)
    interval = args.interval or defaults.INTERVAL
    monitor = args.monitor or []
    debug = args.debug or 'warn'
    api_client = docker.APIClient(base_url=host)
