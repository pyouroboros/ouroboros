container_object = {
    'Id': 'cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823',
    'Created': '2018-10-10T23:44:37.08670368Z',
    'Path': 'tail',
    'Args': [
        '-f',
        '/dev/null'
    ],
    'State': {
        'Status': 'running',
        'Running': True,
        'Paused': False,
        'Restarting': False,
        'OOMKilled': False,
        'Dead': False,
        'Pid': 9400,
        'ExitCode': 0,
        'Error': '',
        'StartedAt': '2018-10-10T23:44:37.806175342Z',
        'FinishedAt': '0001-01-01T00:00:00Z'
    },
    'Image': 'sha256:59788edf1f3e78cd0ebe6ce1446e9d10788225db3dedcfd1a59f764bad2b2690',
    'ResolvConfPath': '/var/lib/docker/containers/cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823/resolv.conf',
    'HostnamePath': '/var/lib/docker/containers/cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823/hostname',
    'HostsPath': '/var/lib/docker/containers/cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823/hosts',
    'LogPath': '/var/lib/docker/containers/cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823/cdfc1c483343fbfbbc6e645f80d5d76f18631e8d7f06521d03a1c2fac0c9f823-json.log',
    'Name': '/testName1',
    'RestartCount': 0,
    'Driver': 'overlay2',
    'Platform': 'linux',
    'MountLabel': '',
    'ProcessLabel': '',
    'AppArmorProfile': '',
    'ExecIDs': None,
    'HostConfig': {
        'Binds': [
            'container.py:/tmp/container.py'
        ],
        'ContainerIDFile': '',
        'LogConfig': {
            'Type': 'json-file',
            'Config': {}
        },
        'NetworkMode': 'default',
        'PortBindings': {
            '8080/tcp': [
                {
                    'HostIp': '',
                    'HostPort': '1234'
                }
            ]
        },
        'RestartPolicy': {
            'Name': 'unless-stopped',
            'MaximumRetryCount': 0
        },
        'AutoRemove': False,
        'VolumeDriver': '',
        'VolumesFrom': None,
        'CapAdd': None,
        'CapDrop': None,
        'Dns': [],
        'DnsOptions': [],
        'DnsSearch': [],
        'ExtraHosts': None,
        'GroupAdd': None,
        'IpcMode': 'shareable',
        'Cgroup': '',
        'Links': None,
        'OomScoreAdj': 0,
        'PidMode': '',
        'Privileged': False,
        'PublishAllPorts': False,
        'ReadonlyRootfs': False,
        'SecurityOpt': None,
        'UTSMode': '',
        'UsernsMode': '',
        'ShmSize': 67108864,
        'Runtime': 'runc',
        'ConsoleSize': [
            0,
            0
        ],
        'Isolation': '',
        'CpuShares': 0,
        'Memory': 0,
        'NanoCpus': 0,
        'CgroupParent': '',
        'BlkioWeight': 0,
        'BlkioWeightDevice': [],
        'BlkioDeviceReadBps': None,
        'BlkioDeviceWriteBps': None,
        'BlkioDeviceReadIOps': None,
        'BlkioDeviceWriteIOps': None,
        'CpuPeriod': 0,
        'CpuQuota': 0,
        'CpuRealtimePeriod': 0,
        'CpuRealtimeRuntime': 0,
        'CpusetCpus': '',
        'CpusetMems': '',
        'Devices': [],
        'DeviceCgroupRules': None,
        'DiskQuota': 0,
        'KernelMemory': 0,
        'MemoryReservation': 0,
        'MemorySwap': 0,
        'MemorySwappiness': None,
        'OomKillDisable': False,
        'PidsLimit': 0,
        'Ulimits': None,
        'CpuCount': 0,
        'CpuPercent': 0,
        'IOMaximumIOps': 0,
        'IOMaximumBandwidth': 0,
        'MaskedPaths': [
            '/proc/acpi',
            '/proc/kcore',
            '/proc/keys',
            '/proc/latency_stats',
            '/proc/timer_list',
            '/proc/timer_stats',
            '/proc/sched_debug',
            '/proc/scsi',
            '/sys/firmware'
        ],
        'ReadonlyPaths': [
            '/proc/asound',
            '/proc/bus',
            '/proc/fs',
            '/proc/irq',
            '/proc/sys',
            '/proc/sysrq-trigger'
        ]
    },
    'GraphDriver': {
        'Data': {
            'LowerDir': '/var/lib/docker/overlay2/b71008f360c44cf922a40e3d65f31ded2202586ec916568724b345610f4e9c16-init/diff:/var/lib/docker/overlay2/78efac45259ab15e57b7a2939e0f7bf452cc2a0f842609a3f940927d60291c12/diff',
            'MergedDir': '/var/lib/docker/overlay2/b71008f360c44cf922a40e3d65f31ded2202586ec916568724b345610f4e9c16/merged',
            'UpperDir': '/var/lib/docker/overlay2/b71008f360c44cf922a40e3d65f31ded2202586ec916568724b345610f4e9c16/diff',
            'WorkDir': '/var/lib/docker/overlay2/b71008f360c44cf922a40e3d65f31ded2202586ec916568724b345610f4e9c16/work'
        },
        'Name': 'overlay2'
    },
    'Mounts': [
        {
            'Type': 'volume',
            'Name': 'container.py',
            'Source': '/var/lib/docker/volumes/container.py/_data',
            'Destination': '/tmp/container.py',
            'Driver': 'local',
            'Mode': 'z',
            'RW': True,
            'Propagation': ''
        }
    ],
    'Config': {
        'Hostname': 'cdfc1c483343',
        'Domainname': '',
        'User': '',
        'AttachStdin': False,
        'AttachStdout': False,
        'AttachStderr': False,
        'ExposedPorts': {
            '8080/tcp': {}
        },
        'Tty': False,
        'OpenStdin': False,
        'StdinOnce': False,
        'Env': [
            'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
            'testEnvVar=testVar',
        ],
        'Cmd': [
            'tail',
            '-f',
            '/dev/null'
        ],
        'Image': 'busybox:1.29.3',
        'Volumes': None,
        'WorkingDir': '',
        'Entrypoint': None,
        'OnBuild': None,
        'Labels': {}
    },
    'NetworkSettings': {
        'Bridge': '',
        'SandboxID': '9b2e269ac290d3534dc48bf762ac4654e9ecc5a11b0629a8430b7a6784091f4e',
        'HairpinMode': False,
        'LinkLocalIPv6Address': '',
        'LinkLocalIPv6PrefixLen': 0,
        'Ports': {
            '8080/tcp': [
                {
                    'HostIp': '0.0.0.0',
                    'HostPort': '1234'
                }
            ]
        },
        'SandboxKey': '/var/run/docker/netns/9b2e269ac290',
        'SecondaryIPAddresses': None,
        'SecondaryIPv6Addresses': None,
        'EndpointID': '8c419f386adaeb9da6128b4c5b2e682bcdaaa1ccddbfa655d8c870e75076e536',
        'Gateway': '172.17.0.1',
        'GlobalIPv6Address': '',
        'GlobalIPv6PrefixLen': 0,
        'IPAddress': '172.17.0.2',
        'IPPrefixLen': 16,
        'IPv6Gateway': '',
        'MacAddress': '02:42:ac:11:00:02',
        'Networks': {
            'bridge': {
                'IPAMConfig': None,
                'Links': None,
                'Aliases': None,
                'NetworkID': 'f5117b1618ba5a0b4dea155937e926f380c8cc57cdcab34ae22d6e4862606fc4',
                'EndpointID': '8c419f386adaeb9da6128b4c5b2e682bcdaaa1ccddbfa655d8c870e75076e536',
                'Gateway': '172.17.0.1',
                'IPAddress': '172.17.0.2',
                'IPPrefixLen': 16,
                'IPv6Gateway': '',
                'GlobalIPv6Address': '',
                'GlobalIPv6PrefixLen': 0,
                'MacAddress': '02:42:ac:11:00:02',
                'DriverOpts': None
            }
        }
    }
}