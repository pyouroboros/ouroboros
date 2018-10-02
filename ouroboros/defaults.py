INTERVAL = 300
LOCAL_UNIX_SOCKET = 'unix://var/run/docker.sock'
RESTART_POLICY = {
    'name': 'on-failure',
    'MaximumRetryCount': 1
}