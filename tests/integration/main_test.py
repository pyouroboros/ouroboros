import docker
import imp
import pytest
import Ouroboros.defaults as defaults

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


def test_create_container():
    api_client.pull(repository=test_repo, tag=test_tag)
    networking_config = api_client.create_networking_config({test_network: api_client.create_endpoint_config()})

    host_config = api_client.create_host_config(
        binds=[f"{test_container_props['volumes'][0]}:{test_container_mount_dest}"],
        port_bindings={test_container_props['ports'][0]: test_host_port}
    )

    api_client.create_container(**test_container_props, networking_config=networking_config, host_config=host_config)
    api_client.create_container(image=test_image, command='tail -f /dev/null', name='ignoreme')

    api_client.start(test_container_name)
    api_client.start('ignoreme')

    first_container = api_client.containers(filters={'name': test_container_name})[0]
    second_container = api_client.containers(filters={'name': 'ignoreme'})[0]

    assert first_container['State'] == 'running' and second_container['State'] == 'running'
    assert first_container['Id'] in api_client.inspect_network(test_network)['Containers']


def test_main(mocker, caplog):
    mocker.patch('sys.argv', [''])
    mocker.patch.dict('os.environ',
                      {'INTERVAL': '1',
                       'LOGLEVEL': 'debug',
                       'RUNONCE': 'true',
                       'CLEANUP': 'true',
                       'IGNORE': 'ignoreme',
                       'MONITOR': test_container_name})
    with pytest.raises(SystemExit):
        assert imp.load_source('__main__', 'ouroboros/ouroboros') == SystemExit

    assert f"Could not clean up image: {test_image}" in caplog.text


def test_container_updated(mocker):
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


def test_container_not_updated():
    ignored_container = api_client.containers(filters={'name': 'ignoreme'})[0]
    insp = api_client.inspect_container(ignored_container)

    assert insp['Config']['Image'] == f'{test_image}'


def test_rm_updated_container():
    running_container = api_client.containers(
        filters={'name': test_container_name})[0]
    api_client.stop(running_container)
    api_client.remove_container(running_container)
    assert api_client.containers(filters={'name': test_container_name}) == []

    ignored_container = api_client.containers(filters={'name': 'ignoreme'})[0]
    api_client.stop(ignored_container)
    api_client.remove_container(ignored_container)
    assert api_client.containers(filters={'name': 'ignoreme'}) == []


def test_rm_test_images():
    images = [test_image, f'{test_repo}:latest']
    for image in images:
        if api_client.images(image):
            api_client.remove_image(image)
            assert api_client.images(name=image) == []


def test_rm_network():
    api_client.remove_network(test_network)
    assert api_client.networks(names=test_network) == []
