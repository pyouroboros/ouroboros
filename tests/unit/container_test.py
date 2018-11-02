import pytest
import ouroboros.container as container
from container_object import container_object
import docker
import ouroboros.defaults

@pytest.fixture()
def fake_container():
    return container_object


def test_new_container_properties(fake_container):
    latest = 'busybox:latest'
    new_container = container.new_container_properties(
        fake_container, new_image=latest)
    assert new_container['name'] == 'testName1'
    assert new_container['image'] == latest
    assert new_container['host_config'] == fake_container['HostConfig']
    assert new_container['labels'] == fake_container['Config']['Labels']
    assert new_container['entrypoint'] == fake_container['Config']['Entrypoint']
    assert new_container['environment'] == fake_container['Config']['Env']


def test_get_name(fake_container):
    assert container.get_name(fake_container) == 'testName1'


@pytest.mark.parametrize('monitor_args, ignore_args, mon_result, expected_caplog', [
    (["test1", "test2"], ["test3", "test4"], ["test1", "test2"], False),
    (["test1"], ["test1", "test2"], [], True),
    ([], [], [], False),
    ([], ["test1"], [], False),
    (["test1"], [], ["test1"], False)
])
def test_reconcile_monitor_ignore(caplog, monitor_args, ignore_args, mon_result, expected_caplog):
    result = container.reconcile_monitor_ignore(monitor_args, ignore_args)
    assert result == mon_result
    if expected_caplog:
        assert "specified in monitor and ignore." in caplog.text
        assert "Container(s) will not be updated." in caplog.text


def test_to_monitor(mocker):
    mock_client = mocker.Mock(spec=docker.APIClient)
    mock_client.base_url = ouroboros.defaults.LOCAL_UNIX_SOCKET
    mock_client.containers.return_value = []

    result = container.to_monitor(monitor='test', api_client=mock_client)
    assert result == []
    mock_client.containers.assert_called_once()


def test_to_monitor_exception(mocker, caplog):
    mock_client = mocker.Mock(spec=docker.APIClient)
    mock_client.base_url = ouroboros.defaults.LOCAL_UNIX_SOCKET
    mock_client.containers.side_effect = BaseException('I blew up!!')

    container.to_monitor(monitor='test', api_client=mock_client)
    assert 'connect to Docker API' in caplog.text


def test_running_exception(mocker, caplog):
    mock_client = mocker.Mock(spec=docker.APIClient)
    mock_client.base_url = ouroboros.defaults.LOCAL_UNIX_SOCKET
    mock_client.containers.side_effect = BaseException("I'm blasting off again!")

    container.running(mock_client)
    assert 'connect to Docker API' in caplog.text
