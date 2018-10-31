import docker
import pytest
from importlib.machinery import SourceFileLoader
import ouroboros.defaults as defaults

api_client = docker.APIClient(defaults.LOCAL_UNIX_SOCKET)

test_network = 'test_network'
test_repo = 'busybox'
test_tag = '1.28'
test_image = f'{test_repo}:{test_tag}'
test_container_name = f'{test_repo}_test'
test_host_port = 1234
test_container_mount_dest = '/tmp'
test_container_props = {
    'name': test_container_name,
    'image': test_image,
    'command': 'tail -f /dev/null',
    'detach': True,
    'ports': [
        '5678'
    ],
    'environment': [
        'testEnvVar=testVar'
    ],
    'volumes': [
        '/tmp'
    ]
}


def test_create_network():
    api_client.create_network(test_network)
    assert api_client.inspect_network(test_network)['Name'] == test_network


@pytest.fixture()
def create_container():
        api_client.pull(repository=test_repo, tag=test_tag)
        api_client.create_container(**test_container_props, networking_config=api_client.create_networking_config({test_network: api_client.create_endpoint_config()}),
                                    host_config=api_client.create_host_config(binds=[f"{test_container_props['volumes'][0]}:{test_container_mount_dest}"],
                                                                            port_bindings={test_container_props['ports'][0]: test_host_port}))
        api_client.start(test_container_name)
        running_container = api_client.containers(filters={'name': test_container_name})[0]


def test_main_with_latest(mocker, create_container):
    mocker.patch('sys.argv', [''])
    mocker.patch.dict('os.environ',
                      {'INTERVAL': '1',
                       'LOGLEVEL': 'debug',
                       'RUNONCE': 'true',
                       'CLEANUP': 'true',
                       'MONITOR': test_container_name})
    with pytest.raises(SystemExit):
        assert SourceFileLoader('__main__', 'ouroboros/ouroboros').load_module() == SystemExit


def test_image_cleanup():
    assert api_client.images(name=test_image) == []


def test_container_updated_to_latest(mocker):
    running_container = api_client.containers(
        filters={'name': test_container_name})[0]
    new_container = api_client.inspect_container(running_container)
    host_port = new_container['HostConfig']['PortBindings'][
        f"{test_container_props['ports'][0]}/tcp"][0]['HostPort']
    assert new_container['State']['Status'] == 'running'
    assert new_container['Config']['Image'] == f'{test_repo}:latest'
    assert new_container['Config']['Cmd'] == test_container_props['command'].split()
    assert test_container_props['environment'][0] in new_container['Config']['Env']
    assert new_container['Mounts'][0]['Source'] == test_container_props['volumes'][0]
    assert new_container['Mounts'][0]['Destination'] == test_container_mount_dest
    assert host_port == str(test_host_port)


def test_rm_updated_container_latest():
    running_container = api_client.containers(
        filters={'name': test_container_name})[0]
    api_client.stop(running_container)
    api_client.remove_container(running_container)
    assert api_client.containers(filters={'name': test_container_name}) == []


@pytest.mark.script_launch_mode('subprocess')
def test_main_with_keeptag(mocker, create_container, script_runner):
    mocker.patch.dict('os.environ',
                      {'INTERVAL': '1',
                       'LOGLEVEL': 'debug',
                       'RUNONCE': 'true',
                       'CLEANUP': 'true',
                       'KEEPTAG': 'true',
                       'MONITOR': test_container_name})
    status = script_runner.run('ouroboros')
    assert status.success


def test_container_updated_with_same_tag(mocker):
    running_container = api_client.containers(
        filters={'name': test_container_name})[0]
    new_container = api_client.inspect_container(running_container)
    host_port = new_container['HostConfig']['PortBindings'][
        f"{test_container_props['ports'][0]}/tcp"][0]['HostPort']
    assert new_container['State']['Status'] == 'running'
    assert new_container['Config']['Image'] == test_image
    assert new_container['Config']['Cmd'] == test_container_props['command'].split()
    assert test_container_props['environment'][0] in new_container['Config']['Env']
    assert new_container['Mounts'][0]['Source'] == test_container_props['volumes'][0]
    assert new_container['Mounts'][0]['Destination'] == test_container_mount_dest
    assert host_port == str(test_host_port)


def test_rm_updated_container_with_same_tag():
    running_container = api_client.containers(
        filters={'name': test_container_name})[0]
    api_client.stop(running_container)
    api_client.remove_container(running_container)
    assert api_client.containers(filters={'name': test_container_name}) == []


def test_rm_network():
    api_client.remove_network(test_network)
    assert api_client.networks(names=test_network) == []
