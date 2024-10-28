from ionwizard.validate import get_library_key, library
from tempfile import TemporaryDirectory
import yaml
import os


def test_get_library_key(mocker):
    config_content = {
        "ionworks": {
            "libraries": [
                {"library": "testlib", "key": "TEST-KEY-123", "install": True}
            ]
        }
    }
    with TemporaryDirectory() as dir_name:
        config_dir = os.path.join(dir_name, "ionworks")
        os.makedirs(config_dir)
        config_path = os.path.join(config_dir, "config.yml")
        with open(config_path, "w") as f:
            yaml.safe_dump(config_content, f)

        mocker.patch("platformdirs.user_config_dir", return_value=config_dir)

        key = get_library_key("testlib")
        assert key == "TEST-KEY-123"

        key = get_library_key("nonexistentlib")
        assert key is None


def test_validate(mocker):
    mocker.patch("ionwizard.validate.get_library_key", return_value="VALID-KEY-123")
    mocker.patch(
        "requests.post",
        return_value=mocker.Mock(
            status_code=200, json=lambda: {"meta": {"code": "VALID"}}
        ),
    )

    result = library("testlib")
    assert result == {"success": True, "message": "License key is valid"}

    mocker.patch("ionwizard.validate.get_library_key", return_value="EXPIRED-KEY-123")
    mocker.patch(
        "requests.post",
        return_value=mocker.Mock(
            status_code=200, json=lambda: {"meta": {"code": "EXPIRED"}}
        ),
    )

    result = library("testlib")
    assert result == {"success": False, "message": "Error: License key expired"}

    mocker.patch("ionwizard.validate.get_library_key", return_value="INVALID-KEY-123")
    mocker.patch(
        "requests.post",
        return_value=mocker.Mock(
            status_code=200, json=lambda: {"meta": {"code": "INVALID"}}
        ),
    )

    result = library("testlib")
    assert result == {"success": False, "message": "Error: Invalid license key"}

    mocker.patch("ionwizard.validate.get_library_key", return_value="VALID-KEY-123")
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=400))

    result = library("testlib")
    assert result == {
        "success": False,
        "message": "Error: Failed to validate license key",
    }
