import sys
import subprocess


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


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        package_name = args[0]
        license_key = args[1]
        address = IonWorksWizard.get_address(license_key)
        print(f"\nPackage URLs:\n\t{address}\n\n")
        if len(args) > 2:
            runPip = args[2]
            if runPip.lower() == "true":
                IonWorksWizard.install_library(package_name, address)
    except IndexError:
        print(
            "\nUsage:\n"
            "\tpython library_wizard.py "
            "<package name> <key> "
            "<install package, optional: true or false>"
        )
