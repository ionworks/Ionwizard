# Project wizard

Ionwizard can be used to install python projects which use a `pyproject.toml`
file. The project wizard does the following:
1. Read the `pyproject.toml`
2. Look for the ionworks license key stored on your machine
3. Install ionworks libraries from the private repositories
4. Install the remaining dependencies and project metadata for the project

## Install with a explicit configuration file

If a library [configuration file](library_installation.md) was provided,
then the configuration file can be passed into the installer:
```bash
ionwizard-install -c <your_config_file>.yml
```
This will read the configuration file and store the license key information
locally so that it can be reused by ionworks applications.

## Install using a saved configuration

If a ionworks configuration file is already stored locally, then the install
tool can be run without any arguments:
```bash
ionwizard-install
```

## Additional pip arguments

Other than the configuration file, all arguments are forwarded to `pip` while
installing the package. For example, to install the dev dependencies in 
editable mode:
```bash
ionwizard-install -c <your_config_file>.yml -e ".[dev]"
```
This command will read the config file, install the ionworks packages,
save the ionworks configuration file, then install the rest of the project in
editable mode with the dev dependencies.
