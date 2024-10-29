import sys
import subprocess
import yaml
from platformdirs import user_config_dir
from pathlib import Path
import machineid
import uuid
from ionwizard.env_variables import KEYGEN_ACCOUNT_ID


class IonWorksPipWizard:
    @staticmethod
    def get_address(key: str):
        head = "https://license:"
        middle = "@api.keygen.sh/v1/accounts/"
        account = KEYGEN_ACCOUNT_ID
        tail = "/engines/pypi/simple"
        return head + key + middle + account + tail

    @staticmethod
    def install_library(lib_name, web_address):
        err = subprocess.call(["pip", "install", lib_name, "--index-url", web_address])
        if err != 0:
            print(f"\nInstallation failed for {lib_name}.\n")

    @staticmethod
    def install_from(config):
        for library in config["libraries"]:
            addr = IonWorksPipWizard.get_address(library["key"])
            if library["install"]:
                IonWorksPipWizard.install_library(library["library"], addr)
            else:
                print(f'\n{library["library"]} --index-url {addr}\n')

    @staticmethod
    def process_config(file_name):
        with open(file_name, "r") as f:
            config = yaml.safe_load(f)
        if "libraries" not in config:
            raise ValueError("Invalid configuration file.")
        return config

    @staticmethod
    def save_config(config):
        config_dir = Path(user_config_dir("ionworks"))
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "config.yml"

        if "user_id" not in config:
            config["user_id"] = str(uuid.uuid4())
        config["machine_id"] = machineid.id()

        print(f"\nSaving configuration to {config_path}\n")

        with open(config_path, "w") as f:
            yaml.dump({"ionworks": config}, f)


def run():
    try:
        config_file = sys.argv[1]
        processed_config = IonWorksPipWizard.process_config(config_file)
        IonWorksPipWizard.install_from(processed_config)
        IonWorksPipWizard.save_config(processed_config)
    except (IndexError, FileNotFoundError):
        print("\nUsage:\n\tpython library_wizard.py <config file>\n")


if __name__ == "__main__":
    run()
