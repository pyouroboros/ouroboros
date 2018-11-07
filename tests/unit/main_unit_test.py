import pytest
from ouroboros.main import main
import docker
import logging
import argparse
from container_object import container_object


@pytest.fixture()
def fake_api(mocker):
    return mocker.Mock(spec=docker.APIClient)


@pytest.fixture()
def fake_namespace(mocker):
    return mocker.Mock(spec=argparse.Namespace)


def test_main_none_running(fake_namespace, fake_api, caplog):
    caplog.set_level(logging.INFO)
    fake_namespace.run_once = True
    fake_api.containers.return_value = []

    main(args=fake_namespace, api_client=fake_api)
    fake_api.containers.assert_called_once()
    assert 'No containers are running' in caplog.text


def test_main_full(fake_namespace, fake_api, caplog):
    caplog.set_level(logging.INFO)

    fake_namespace.run_once = True
    fake_namespace.monitor = ["testName1"]
    fake_namespace.ignore = ["derp"]
    fake_namespace.cleanup = True
    fake_namespace.keep_tag = True

    fake_api.inspect_container.return_value = container_object # called twice
    fake_api.containers.return_value = [container_object] # called twice
    fake_api.inspect_image.side_effect = [{'RepoTags': ["repo:1.1"],
                                           'Id': '1'},
                                          {'RepoTags': ["repo:latest"],
                                           'Id': '2'}] # called twice
    fake_api.create_container.return_value = {'Id': '2'}

    with pytest.raises(SystemExit) as e:
        main(args=fake_namespace, api_client=fake_api)

    assert e.type == SystemExit
    assert e.value.code == 0
    assert 2 == fake_api.containers.call_count
    assert 2 == fake_api.inspect_image.call_count
    assert 2 == fake_api.inspect_container.call_count
    fake_api.pull.assert_called_once()
    fake_api.stop.assert_called_once()
    fake_api.remove_container.assert_called_once()
    fake_api.create_container.assert_called_once()
    fake_api.start.assert_called_once()


def test_main_exception(fake_namespace, fake_api, caplog):
    caplog.set_level(logging.INFO)

    fake_namespace.run_once = True
    fake_namespace.monitor = ["testName1"]
    fake_namespace.ignore = ["derp"]
    fake_namespace.cleanup = True
    fake_namespace.keep_tag = True

    fake_api.inspect_container.return_value = container_object  # called twice
    fake_api.containers.return_value = [container_object]  # called twice
    fake_api.inspect_image.return_value = {'RepoTags': ["repo:1.1"], 'Id': '1'} # called once

    fake_api.pull.side_effect = docker.errors.APIError("I blew up!!")
    fake_api.create_container.return_value = {'Id': '2'}

    with pytest.raises(SystemExit) as e:
        main(args=fake_namespace, api_client=fake_api)

    assert e.type == SystemExit
    assert e.value.code == 0
    assert 2 == fake_api.containers.call_count
    assert 2 == fake_api.inspect_container.call_count
    fake_api.inspect_image.assert_called_once()
    fake_api.pull.assert_called_once()
