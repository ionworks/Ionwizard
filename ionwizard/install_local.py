import sys
import copy
import subprocess
import toml
from ionwizard.validate import read_config_libraries
from ionwizard.library_wizard import IonWorksPipWizard
import tempfile
from pathlib import Path


class IonWorksInstallWizard(IonWorksPipWizard):
    """
    Install a project from a pyproject.toml file, while installing ionworks
    dependencies separately.
    """

    def collect_libraries_to_install(self):
        if len(sys.argv) > 1:
            if ".yml" in sys.argv[1]:
                config_file = sys.argv[1]
                processed_config = self.process_config(config_file)
                self.save_config(processed_config)
        libraries = read_config_libraries()
        return libraries

    @staticmethod
    def copy_local_pyproject_file():
        with open("pyproject.toml", "r") as f:
            original_pyproject_toml = toml.load(f)
        return copy.deepcopy(original_pyproject_toml)

    @staticmethod
    def install_libraries_from_config(libraries, pyproject_file):
        for idx, dep in enumerate(pyproject_file["project"]["dependencies"]):
            for library in libraries:
                if dep.startswith(library["library"]):
                    # Remove the dependency from the list to be installed from pip
                    del pyproject_file["project"]["dependencies"][idx]
                    # Install the library from the license config
                    addr = IonWorksPipWizard.get_address(library["key"])
                    IonWorksPipWizard.install_library(dep, addr)

    @staticmethod
    def install_from_pyproject(pyproject_file):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_config = Path(temp_dir) / "pyproject.toml"
            with open(temp_config, "w") as f:
                toml.dump(pyproject_file, f)
            cmd = [
                "pip",
                "install",
                "-e",
                ".",
                f"--config-settings=pyproject_toml={temp_config}",
            ]
            subprocess.run(cmd)


def run():
    libraries = IonWorksInstallWizard().collect_libraries_to_install()
    new_pyproject = IonWorksInstallWizard.copy_local_pyproject_file()
    IonWorksInstallWizard.install_libraries_from_config(libraries, new_pyproject)
    IonWorksInstallWizard.install_from_pyproject(new_pyproject)


if __name__ == "__main__":
    run()
