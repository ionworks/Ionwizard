from ionwizard.library_wizard import IonWorksWizard
import pytest
from tempfile import TemporaryDirectory
import yaml
import os


def test_bad_config():
    config_file = {"bad_name": [{'library': 'package1', 'key': 'XXX-YYY-ZZZ', 'install': False}]}
    with TemporaryDirectory() as dir_name:
        file_name = os.path.join(dir_name, "test.yml")
        with open(file_name, "w") as f:
            yaml.safe_dump(config_file, f)
        with pytest.raises(KeyError):
            IonWorksWizard.process_config(file_name)

