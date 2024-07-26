import os
import tempfile
from unittest.mock import patch

import pytest

from jumpstarter.config import ClientConfig, ClientConfigDrivers, UserConfig


def test_user_config_exists():
    assert UserConfig.exists() is False
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("")
        f.close()
        UserConfig.USER_CONFIG_PATH = f.name
        assert UserConfig.exists() is True
        os.unlink(f.name)


def test_user_config_load():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config:
  current-client: testclient
"""
    with patch.object(
        ClientConfig, "load", return_value=ClientConfig("testclient", "abc", "123", ClientConfigDrivers([], False))
    ) as mock_load:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(USER_CONFIG)
            f.close()
            UserConfig.USER_CONFIG_PATH = f.name
            config = UserConfig.load()
            mock_load.assert_called_once_with("testclient")
            assert config.current_client.name == "testclient"
            os.unlink(f.name)


def test_user_config_load_does_not_exist():
    with pytest.raises(FileNotFoundError):
        _ = UserConfig.load()


def test_user_config_load_no_current_client():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config: {}
"""
    with patch.object(
        ClientConfig, "load", return_value=ClientConfig("testclient", "abc", "123", ClientConfigDrivers([], False))
    ) as mock_load:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(USER_CONFIG)
            f.close()
            UserConfig.USER_CONFIG_PATH = f.name
            config = UserConfig.load()
            mock_load.assert_not_called()
            assert config.current_client is None
            os.unlink(f.name)


def test_user_config_load_current_client_empty():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config:
    current-client: ""
"""
    with patch.object(
        ClientConfig, "load", return_value=ClientConfig("testclient", "abc", "123", ClientConfigDrivers([], False))
    ) as mock_load:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(USER_CONFIG)
            f.close()
            UserConfig.USER_CONFIG_PATH = f.name
            config = UserConfig.load()
            mock_load.assert_not_called()
            assert config.current_client is None
            os.unlink(f.name)


def test_user_config_load_invalid_api_version_raises():
    USER_CONFIG = """apiVersion: abc
kind: UserConfig
config:
  current-client: testclient
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(USER_CONFIG)
        f.close()
        UserConfig.USER_CONFIG_PATH = f.name
        with pytest.raises(ValueError):
            _ = UserConfig.load()
        os.unlink(f.name)


def test_user_config_load_invalid_kind_raises():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: ClientConfig
config:
  current-client: testclient
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(USER_CONFIG)
        f.close()
        UserConfig.USER_CONFIG_PATH = f.name
        with pytest.raises(ValueError):
            _ = UserConfig.load()
        os.unlink(f.name)


def test_user_config_load_no_config_raises():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(USER_CONFIG)
        f.close()
        UserConfig.USER_CONFIG_PATH = f.name
        with pytest.raises(ValueError):
            _ = UserConfig.load()
        os.unlink(f.name)


def test_user_config_save():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config:
  current-client: testclient
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        UserConfig.USER_CONFIG_PATH = f.name
        config = UserConfig(ClientConfig("testclient", "abc", "123", ClientConfigDrivers([], False)))
        UserConfig.save(config)
        with open(f.name) as loaded:
            value = loaded.read()
            assert value == USER_CONFIG
        os.unlink(f.name)


def test_user_config_save_no_current_client():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config:
  current-client: ''
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        UserConfig.USER_CONFIG_PATH = f.name
        config = UserConfig(None)
        UserConfig.save(config)
        with open(f.name) as loaded:
            value = loaded.read()
            assert value == USER_CONFIG
        os.unlink(f.name)


def test_user_config_use_client():
    USER_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
config:
  current-client: testclient
"""
    with patch.object(
        ClientConfig, "load", return_value=ClientConfig("testclient", "abc", "123", ClientConfigDrivers([], False))
    ) as mock_load:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(USER_CONFIG)
            f.close()
            UserConfig.USER_CONFIG_PATH = f.name
            config = UserConfig(ClientConfig("another", "abc", "123", ClientConfigDrivers([], False)))
            config.use_client("testclient")
            with open(f.name) as loaded:
                value = loaded.read()
                assert value == USER_CONFIG
                mock_load.assert_called_once_with("testclient")
            assert config.current_client.name == "testclient"
            os.unlink(f.name)
