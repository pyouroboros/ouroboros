import defaults
import argparse

host = ''
interval = ''
monitor = []
debug = ''

def parser():
    nonlocal host, interval, monitor, debug
    parser = argparse.ArgumentParser(description='ouroboros')
    parser.add_argument('-h','--host', help='Local socket for remote tcp host (defaults to "unix://var/run/docker.sock")', required=False)
    parser.add_argument('-i','--interval', type=int, help='Interval in seconds between checking for updates (defaults to 20s)', required=False)
    parser.add_argument('-m','--monitor', nargs='*', help='Which container to monitor (defaults to all).  Pass in list like -m "container1 container2 etc"', required=False)
    parser.add_argument('-d','--debug', choices=['notset','debug','info', 'warn', 'error', 'critical'], help='Change logger mode to debug (defaults to off)', required=False)
    args = parser.parse_args()
    host = args.host or defaults.LOCAL_UNIX_SOCKET
    if (args.interval
    interval = args.interval or defaults.INTERVAL
    monitor = args.monitor or []
    debug = args.debug or ''
