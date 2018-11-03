import pytest
from ouroboros.main import main
import docker
import logging
import argparse


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

