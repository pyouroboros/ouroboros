import yaml

from pyouroboros import VERSION

org = 'pyouroboros'
project = 'ouroboros'
namespace = "{}/{}".format(org, project)

yaml_arr = []
tags = ['latest', VERSION]

# Docker image, arch, variant, os
arch_list = [('arm', 'arm', 'v6', 'linux'),
             ('armhf', 'arm', 'v7', 'linux'),
             ('arm64', 'arm64', 'v8', 'linux'),
             ('amd64', 'amd64', None, 'linux')]

for tag in tags:
    yaml_doc = {
        'image': '{}:{}'.format(namespace, tag),
        'manifests': []
    }
    for arch in arch_list:
        info = {
            'image': "{}:{}-{}".format(namespace, tag, arch[0]),
            'platform': {
                'architecture': arch[1],
                'os': arch[3]
            }
        }
        if arch[2]:
                info['platform']['variant'] = arch[2]
        yaml_doc['manifests'].append(info)
    yaml_arr.append(yaml_doc)

with open(f".manifest.yaml", 'w') as file:
    yaml.dump_all(yaml_arr, file, default_flow_style=False)
