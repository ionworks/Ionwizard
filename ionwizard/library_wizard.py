import sys
import subprocess
import yaml


class IonWorksWizard:
    @staticmethod
    def get_address(key: str):
        head = "https://license:"
        middle = "@api.keygen.sh/v1/accounts/"
        account = "b1b31816-7a41-4fc0-8dd3-a957d1f7bef3"
        tail = "/engines/pypi/simple"
        return head + key + middle + account + tail

    @staticmethod
    def install_library(lib_name, web_address):
        err = subprocess.call(["pip", "install", lib_name, "--index-url", web_address])
        if err != 0:
            print(f"\nInstallation failed for {lib_name}.\n")

    @staticmethod
    def install_from(config):
        for pack in config:
            addr = IonWorksWizard.get_address(pack["key"])
            if pack["install"] == "True":
                IonWorksWizard.install_library(pack["library"], addr)
            else:
                print(f'\n{pack["library"]} --index-url {addr}\n')

    @staticmethod
    def process_config(file_name):
        with open(file_name, "r") as f:
            try:
                return yaml.safe_load(f)["libraries"]
            except KeyError:
                print("\nInvalid configuration file.\n")


def run():
    try:
        config_file = sys.argv[1]
        IonWorksWizard.install_from(IonWorksWizard.process_config(config_file))
    except (IndexError, FileNotFoundError, KeyError):
        print("\nUsage:\n\tpython library_wizard.py <config file>\n")


if __name__ == "__main__":
    run()
