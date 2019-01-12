import pyouroboros.image as image
import docker


def test_image_check_credentials_no_env_var():
    assert not image.check_credentials()


def test_image_check_credentials_env_var(mocker):
    mocker.patch.dict('os.environ', {'REPO_USER': 'test_user', 'REPO_PASS': 'test_pass'})
    assert image.check_credentials() == {'password': 'test_pass', 'username': 'test_user'}


def test_image_check_credentials_false_env_var(mocker):
    mocker.patch.dict('os.environ', {'REPO_USR': 'test_user', 'REPO_PaSS': 'test_pass'})
    assert not image.check_credentials()


def test_image_is_up_to_date():
    old_sha = 'sha256:34ea7509dcad10aa92310f2b41e3afbabed0811ee3a902d6d49cb90f075fe444'
    new_sha = 'sha256:196d12cf6ab19273823e700516e98eb1910b03b17840f9d5509f03858484d321'
    assert image.is_up_to_date(old_sha, old_sha)
    assert not image.is_up_to_date(old_sha, new_sha)


def test_remove_exception(mocker, caplog):
    fake_api = mocker.Mock(spec=docker.APIClient)
    fake_api.remove_image.side_effect = docker.errors.DockerException("I'm in use!")

    fake_image = {'RepoTags': ["testcontainer:1.1"]}

    image.remove(fake_image, fake_api)
    fake_api.remove_image.assert_called_once_with(fake_image)
    assert 'Could not clean up image: testcontainer:1.1, reason:' in caplog.text
