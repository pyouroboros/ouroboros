def set_properties(old, new, self_name=None):
    """Store object for spawning new container in place of the one with outdated image"""
    properties = {
        'name': self_name if self_name else old.name,
        'image': new.tags[0],
        'command': old.attrs['Config']['Cmd'],
        'host_config': old.attrs['HostConfig'],
        'labels': old.attrs['Config']['Labels'],
        'entrypoint': old.attrs['Config']['Entrypoint'],
        'environment': old.attrs['Config']['Env']
    }

    return properties
