# Library wizard

The library installation wizard is used to install python packages from
the ionworks package servers.

Script command:
```bash
python library_wizard.py <your_config_file>.yml
```
Command line alias:
```bash
ionwizard-library <your_config_file>.yml
```

## Configuration file

Products licensed by ionworks can be directly installed by the library 
wizard. Each package requires a product name, license key, and a flag to 
indicate if the package should be installed.
```yaml
libraries:
  - library: <Package name>
    key: <License key>
    install: True
  - library: <Package name 2>
    key: <License key 2>
    install: True
```
If the package versions are going to be managed via a requirements file,
then the install flag can be set to "False" to print the input required 
for a manual installation. The library wizard will always install the 
latest version of the packages, so the wizard can also be used to update 
existing packages.

## Pip installation

The Python packages produced by ionworks can be installed via pip.
The ionworks packages are stored on a private server, but can be
installed by using the "--index-url" argument for pip.

```bash
pip install <package name> --index-url <package URL>
```

The URLs for repository can be quite long, so the wizard can be
used to generate the URLs based on the license key.
```yaml
libraries:
  - library: <Package name>
    key: <license key>
    install: False
```

### Pip configuration

Ionworks python libraries can be installed from `pyproject.toml` and 
`requirements.txt` files by configuring pip to use a different index URL.

Create a file named ```pip.conf``` and add the following lines:
```
[global]
index-url = <URL from library wizard>
```

The pip configuration file needs to be exported as an environment
variable to take effect:
```bash
export PIP_CONFIG_FILE=pip.conf
```

Pip will then check for the libraries the Ionworks package servers
before checking PyPi.
