import os
import sys
import subprocess
import yaml
from tempfile import TemporaryDirectory


class IonWorksImageWizard:
    @staticmethod
    def get_zip_name(product: str):
        return product.replace("/", "_") + ".tar.gz"

    @staticmethod
    def get_address(version: str, library: str):
        head = "https://get.keygen.sh/ion-works-com/"
        tail = IonWorksImageWizard.get_zip_name(library)
        return head + version + "/" + tail

    @staticmethod
    def fetch_image(lib_name, web_address, key, location):
        err = subprocess.call(
            ["curl", "-sSLO", "--output-dir", location, "-L", web_address, "-u", key]
        )
        if err != 0:
            raise RuntimeError(f"\nInstallation failed for {lib_name}.\n")

    @staticmethod
    def load_image(product, location):
        zip_name = IonWorksImageWizard.get_zip_name(product)
        err = subprocess.call(
            [f"docker load < {os.path.join(location, zip_name)}"], shell=True
        )
        if err != 0:
            raise RuntimeError(f"\nDocker loading failed for {product}.\n")

    @staticmethod
    def run_image(product, key, version):
        acceptable_codes = [0, 2]
        err = subprocess.call(
            [
                "docker",
                "run",
                "-it",
                "--name",
                product.replace("/", ""),
                "-p",
                "8888:8888",
                "-e",
                f"IONWORKS_LICENSE_KEY={key}",
                f"{product}:{version}",
            ]
        )
        if err not in acceptable_codes:
            raise RuntimeError(f"\nFailed to start {product}, error code: {err}.\n")

    @staticmethod
    def install_from(config):
        if isinstance(config, list):
            raise ValueError(
                "Invalid configuration file. Only 1 docker image can be specified."
            )
        IonWorksImageWizard.make_container(config)
        IonWorksImageWizard.run_image(
            config["product"], config["key"], config["version"]
        )

    @staticmethod
    def make_container(config):
        with TemporaryDirectory() as image_dir:
            addr = IonWorksImageWizard.get_address(config["version"], config["product"])
            IonWorksImageWizard.fetch_image(
                config["product"], addr, f"license:{config['key']}", image_dir
            )
            IonWorksImageWizard.load_image(config["product"], image_dir)

    @staticmethod
    def process_config(file_name):
        with open(file_name, "r") as f:
            try:
                return yaml.safe_load(f)["docker"]
            except KeyError:
                raise ValueError("Invalid configuration file.")


def run():
    try:
        config_file = sys.argv[1]
        IonWorksImageWizard.install_from(
            IonWorksImageWizard.process_config(config_file)
        )
    except (IndexError, FileNotFoundError):
        print("\nUsage:\n\tpython container_wizard.py <config file>\n")


if __name__ == "__main__":
    run()
