# Project wizard

Ionwizard can be used to install python projects which use a `pyproject.toml`
file. The project wizard does the following:
1. Read the `pyproject.toml`
2. Look for the ionworks license key stored on your machine
3. Install ionworks libraries from the private repositories
4. Install the remaining dependencies and project metadata for the project in
   editable mode

## Install with a explicit configuration file

If a library [configuration file](library_installation.md) was provided,
then the configuration file can be passed into the installer:
```bash
ionwizard-install <your_config_file>.yml
```
This will read the configuration file and store the license key information
locally so that it can be reused by ionworks applications.

## Install using a saved configuration

If a ionworks configurate file is already stored locally, then the install
tool can be run without any arguments:
```bash
ionwizard-install
```
