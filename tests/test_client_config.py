import os
import tempfile
from unittest.mock import patch

import pytest

from jumpstarter.config import ClientConfig
from jumpstarter.config.client import ClientConfigDrivers
from jumpstarter.config.env import JMP_DRIVERS_ALLOW, JMP_ENDPOINT, JMP_TOKEN


def setup_function():
    for key in [
        JMP_TOKEN,
        JMP_ENDPOINT,
        JMP_DRIVERS_ALLOW,
    ]:
        if key in os.environ:
            del os.environ[key]

def test_client_config_try_from_env():
    os.environ[JMP_TOKEN] = "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    os.environ[JMP_ENDPOINT] = "grpcs://jumpstarter.my-lab.com:1443"
    os.environ[JMP_DRIVERS_ALLOW] = "jumpstarter.drivers.*,vendorpackage.*"
    
    config = ClientConfig.try_from_env()
    assert config.name == "default"
    assert config.token == "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    assert config.endpoint == "grpcs://jumpstarter.my-lab.com:1443"
    assert config.drivers.allow == ["jumpstarter.drivers.*", "vendorpackage.*"]
    assert config.drivers.unsafe is False

def test_client_config_try_from_env_not_set():
    config = ClientConfig.try_from_env()
    assert config is None

def test_client_config_from_env():
    os.environ[JMP_TOKEN] = "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    os.environ[JMP_ENDPOINT] = "grpcs://jumpstarter.my-lab.com:1443"
    os.environ[JMP_DRIVERS_ALLOW] = "jumpstarter.drivers.*,vendorpackage.*"
    
    config = ClientConfig.from_env()
    assert config.name == "default"
    assert config.token == "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    assert config.endpoint == "grpcs://jumpstarter.my-lab.com:1443"
    assert config.drivers.allow == ["jumpstarter.drivers.*", "vendorpackage.*"]
    assert config.drivers.unsafe is False

def test_client_config_from_env_allow_unsafe():
    os.environ[JMP_TOKEN] = "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    os.environ[JMP_ENDPOINT] = "grpcs://jumpstarter.my-lab.com:1443"
    os.environ[JMP_DRIVERS_ALLOW] = "UNSAFE"
    
    config = ClientConfig.from_env()
    assert config.name == "default"
    assert config.token == "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    assert config.endpoint == "grpcs://jumpstarter.my-lab.com:1443"
    assert config.drivers.allow == []
    assert config.drivers.unsafe is True

def test_client_config_from_env_no_token_raises():
    os.environ[JMP_ENDPOINT] = "grpcs://jumpstarter.my-lab.com:1443"
    os.environ[JMP_DRIVERS_ALLOW] = "jumpstarter.drivers.*,vendorpackage.*"
     
    with pytest.raises(ValueError):
        _ = ClientConfig.from_env()

def test_client_config_from_env_no_endpoint_raises():
    os.environ[JMP_TOKEN] = "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
    os.environ[JMP_DRIVERS_ALLOW] = "jumpstarter.drivers.*,vendorpackage.*"
     
    with pytest.raises(ValueError):
        _ = ClientConfig.from_env()


def test_client_config_from_file():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
      - jumpstarter.drivers.*
      - vendorpackage.*
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        config = ClientConfig.from_file(f.name)
        assert config.name == f.name.split("/")[-1]
        assert config.endpoint == "grpcs://jumpstarter.my-lab.com:1443"
        assert (
            config.token
            == "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK"
        )
        assert config.drivers.allow == ["jumpstarter.drivers.*", "vendorpackage.*"]
        assert config.drivers.unsafe is False
        os.unlink(f.name)


def test_client_config_from_file_invalid_api_version_raises():
    CLIENT_CONFIG = """apiVersion: abc
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
      - jumpstarter.drivers.*
      - vendorpackage.*
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_invalid_kind_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: UserConfig
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
      - jumpstarter.drivers.*
      - vendorpackage.*
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_no_client_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_no_token_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  drivers:
    allow:
      - jumpstarter.drivers.*
      - vendorpackage.*
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_no_endpoint_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  token: asbfasdf
  drivers:
    allow:
      - jumpstarter.drivers.*
      - vendorpackage.*
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_no_drivers_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_from_file_drivers_allow_not_list_raises():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow: abc
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(CLIENT_CONFIG)
        f.close()
        with pytest.raises(ValueError):
            _ = ClientConfig.from_file(f.name)
        os.unlink(f.name)


def test_client_config_load():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("")
        f.close()
        with patch.object(ClientConfig, "_get_path", return_value=f.name) as _get_path_mock:
            with patch.object(
                ClientConfig,
                "from_file",
                return_value=ClientConfig("another", "abc", "123", ClientConfigDrivers([], False)),
            ) as from_file_mock:
                value = ClientConfig.load("another")
        assert value.name == "another"
        _get_path_mock.assert_called_once_with("another")
        from_file_mock.assert_called_once_with(f.name)
        os.unlink(f.name)


def test_client_config_load_not_found_raises():
    with pytest.raises(FileNotFoundError):
        _ = ClientConfig.load("1235jklhbafsvd90u1234fsad")


def test_client_config_save():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
    - jumpstarter.drivers.*
    - vendorpackage.*
"""
    config = ClientConfig(
        "testclient",
        "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK",
        "grpcs://jumpstarter.my-lab.com:1443",
        ClientConfigDrivers(["jumpstarter.drivers.*", "vendorpackage.*"], False),
    )
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        with patch.object(ClientConfig, "_get_path", return_value=f.name) as _get_path_mock:
            ClientConfig.save(config)
            with open(f.name) as loaded:
                value = loaded.read()
                assert value == CLIENT_CONFIG
        _get_path_mock.assert_called_once_with("testclient")
        os.unlink(f.name)


def test_client_config_save_explicit_path():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
    - jumpstarter.drivers.*
    - vendorpackage.*
"""
    config = ClientConfig(
        "testclient",
        "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK",
        "grpcs://jumpstarter.my-lab.com:1443",
        ClientConfigDrivers(["jumpstarter.drivers.*", "vendorpackage.*"], False),
    )
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        ClientConfig.save(config, f.name)
        with open(f.name) as loaded:
            value = loaded.read()
            assert value == CLIENT_CONFIG
        os.unlink(f.name)


def test_client_config_save_unsafe_drivers():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    unsafe: true
"""
    config = ClientConfig(
        "testclient",
        "dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK",
        "grpcs://jumpstarter.my-lab.com:1443",
        ClientConfigDrivers([], True),
    )
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        ClientConfig.save(config, f.name)
        with open(f.name) as loaded:
            value = loaded.read()
            assert value == CLIENT_CONFIG
        os.unlink(f.name)


def test_client_config_exists():
    with patch.object(
        ClientConfig, "_get_path", return_value="/users/adsf/.config/jumpstarter/clients/abc.yaml"
    ) as _get_path_mock:
        assert ClientConfig.exists("abc") is False
        _get_path_mock.assert_called_once_with("abc")


def test_client_config_list():
    CLIENT_CONFIG = """apiVersion: jumpstarter.dev/v1alpha1
kind: Client
client:
  endpoint: grpcs://jumpstarter.my-lab.com:1443
  token: dGhpc2lzYXRva2VuLTEyMzQxMjM0MTIzNDEyMzQtc2Rxd3Jxd2VycXdlcnF3ZXJxd2VyLTEyMzQxMjM0MTIzNDEyMzQxMjM0LXF3ZXJxd2VycXdlcnF3ZXJxd2VycXdlcnF3ZXIK
  drivers:
    allow:
    - jumpstarter.drivers.*
    - vendorpackage.*
"""
    d = tempfile.TemporaryDirectory()
    with open(f"{d.name}/testclient.yaml", "w") as f:
        f.write(CLIENT_CONFIG)
        f.close()
    ClientConfig.CLIENT_CONFIGS_PATH = d.name
    configs = ClientConfig.list()
    assert len(configs) == 1
    assert configs[0].name == "testclient"
    d.cleanup()


def test_client_config_list_none():
    with tempfile.TemporaryDirectory() as d:
        ClientConfig.CLIENT_CONFIGS_PATH = d
        configs = ClientConfig.list()
        assert len(configs) == 0


def test_client_config_list_not_found_raises():
    ClientConfig.CLIENT_CONFIGS_PATH = "/asdf/2134/cv/clients"
    with pytest.raises(FileNotFoundError):
        _ = ClientConfig.list()
