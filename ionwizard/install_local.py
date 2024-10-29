import copy
import subprocess
import toml
from ionwizard.validate import read_config_libraries
from ionwizard.library_wizard import IonWorksPipWizard
import tempfile
from pathlib import Path


def run():
    """
    Read the local pyproject.toml file, extract dependencies that are in the license
    config separately, and install them from the license config. Install the rest
    of the dependencies with pip.
    """
    # Read the pyproject.toml file
    with open("pyproject.toml", "r") as f:
        original_pyproject_toml = toml.load(f)

    new_pyproject_toml = copy.deepcopy(original_pyproject_toml)

    # Remove dependencies that are in the license config separately
    libraries = read_config_libraries()
    for idx, dep in enumerate(new_pyproject_toml["project"]["dependencies"]):
        for library in libraries:
            if dep.startswith(library["library"]):
                # Remove the dependency from the list to be installed from pip
                del new_pyproject_toml["project"]["dependencies"][idx]
                # Install the library from the license config
                addr = IonWorksPipWizard.get_address(library["key"])
                IonWorksPipWizard.install_library(dep, addr)

    # Create temporary pyproject.toml file without dependencies installed from license
    # config and use it to install the package
    # Use a context manager to handle the temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_config = Path(temp_dir) / "pyproject.toml"

        # Write the modified config
        with open(temp_config, "w") as f:
            toml.dump(new_pyproject_toml, f)

        cmd = [
            "pip",
            "install",
            "-e",
            ".",
            f"--config-settings=pyproject_toml={temp_config}",
        ]
        subprocess.run(cmd)


if __name__ == "__main__":
    run()
