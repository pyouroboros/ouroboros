import re


def checkuri(uri):
    """Validate tcp:// regex"""
    regex = re.compile(r"""(?xi) # "verbose" mode & case-insensitive
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


def set_properties(old, new):
    """Store object for spawning new container in place of the one with outdated image"""
    properties = {
        'name': old.name,
        'image': new.tags[0],
        'command': old.attrs['Config']['Cmd'],
        'host_config': old.attrs['HostConfig'],
        'labels':  old.attrs['Config']['Labels'],
        'entrypoint':  old.attrs['Config']['Entrypoint'],
        'environment':  old.attrs['Config']['Env']
    }

    return properties

