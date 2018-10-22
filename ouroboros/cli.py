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
    regex = re.compile( r"""(?xi) # "verbose" mode & case-insensitive
        \A                        # in the beginning...
        tcps?://                  # tcp or tcps protocol
        (?:                       # hostname / IP address
         (?:                      # short or FQDN
          (?![-.a-z0-9]{254,})    # up to 253 total chars in identifier
          (?![.0-9]+)             # not completely numeric
          (?:                     # hostname part
           (?=[a-z0-9])           # starts with alnum only
           [-a-z0-9]{1,63}        # 1-63 alphanumeric or hyphen chars
           (?<=[a-z0-9])          # ends with alnum only
          )
          (?:                     # domain name components are less strict
           \.                     # period separator
           [-a-z0-9]{1,63}        # 1-63 alphanumeric or hyphen chars
           (?<!-)                 # doesn't end with a hyphen
          )*                      # zero or more domain components
         )|(?:                    # or an IP address
          (?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}  # 0-255
             (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
         )
        )
        (?::\d{1,5})?             # optional port
        (?:/\S*)?                 # optional path / trailing slash
        \Z
        """)
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
    parser = argparse.ArgumentParser(description='ouroboros', epilog='Example: python3 main.py -u tcp://1.2.3.4:5678 -i 20 -m container1 container2 -l warn')
    parser.add_argument('-u', '--url', help='Url for tcp host (defaults to "unix://var/run/docker.sock")', required=False)
    parser.add_argument('-i', '--interval', type=int, help='Interval in seconds between checking for updates (defaults to 300s)', required=False)
    parser.add_argument('-m', '--monitor', nargs='+', help='Which container to monitor (defaults to all running).', required=False)
    parser.add_argument('-l', '--loglevel', choices=['notset', 'debug', 'info', 'warn', 'error', 'critical'], help='Change logger mode (defaults to info)', required=False)
    parser.add_argument('-r', '--runonce', help='Only run ouroboros once then exit', action='store_true', required=False)
    parser.add_argument('-c', '--cleanup', help='Remove old images after updating', action='store_true', required=False)
    args = parser.parse_args(sysargs)
    if args.url:
        host = args.url
        if not checkURI(host):
            host = defaults.LOCAL_UNIX_SOCKET
    interval = args.interval or get_interval_env() or defaults.INTERVAL
    monitor = args.monitor or environ.get('MONITOR') or []
    loglevel = args.loglevel or environ.get('LOGLEVEL') or 'info'
    run_once = args.runonce or environ.get('RUNONCE') or False
    cleanup = args.cleanup or environ.get('CLEANUP') or False
    api_client = docker.APIClient(base_url=host)
    return args
