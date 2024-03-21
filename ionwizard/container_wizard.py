import sys
import subprocess
import yaml


class IonWorksWizard:
    @staticmethod
    def get_zip_name(product: str):
        return product.replace("/", "_") + ".tar.gz"

    @staticmethod
    def get_address(version: str, library: str):
        head = "https://get.keygen.sh/ion-works-com/"
        tail = IonWorksWizard.get_zip_name(library)
        return head + version + "/" + tail

    @staticmethod
    def fetch_image(lib_name, web_address, key):
        err = subprocess.call(["curl", "-sSLO", "-L", web_address, "-u", key])
        if err != 0:
            raise RuntimeError(f"\nInstallation failed for {lib_name}.\n")

    @staticmethod
    def load_image(product):
        zip_name = IonWorksWizard.get_zip_name(product)
        err = subprocess.call([f"docker load < {zip_name}"], shell=True)
        if err != 0:
            raise RuntimeError(f"\nDocker loading failed for {product}.\n")

    @staticmethod
    def run_image(product, key, version):
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
        if err != 0:
            raise RuntimeError(f"\nFailed to start {product}.\n")

    @staticmethod
    def install_from(config):
        if isinstance(config, list):
            raise ValueError(
                "Invalid configuration file. Only 1 docker image can be specified."
            )
        addr = IonWorksWizard.get_address(config["version"], config["product"])
        IonWorksWizard.fetch_image(config["product"], addr, f"license:{config['key']}")
        IonWorksWizard.load_image(config["product"])
        IonWorksWizard.run_image(config["product"], config["key"], config["version"])

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
        IonWorksWizard.install_from(IonWorksWizard.process_config(config_file))
    except (IndexError, FileNotFoundError):
        print("\nUsage:\n\tpython container_wizard.py <config file>\n")


if __name__ == "__main__":
    run()
