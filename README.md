# Ionworks Installation Wizard

Ionworks products are stored on private repositories. The software in
this project is designed to help users access Ionworks software.

## Installation

The scripts in ionwizard can be run without installing the package, however,
installation can add command line support.
```bash
pip install .
```

### Available commands

Specific details and options for the installation scripts are detailed in their
own sections, but the aliases are explained in this section.

#### Library wizard

The library installation wizard is used to install python packages from
the ionworks package servers.

Script command:
```bash
python library_wizard.py <package name> <key> true
```
Command line alias:
```bash
ionwizard-library <package name> <key> true
```

## Python libraries

The Python packages produced by Ionworks can be installed via pip.
The Ionworks packages are stored on a private server, but can be
installed by using the "--index-url" argument for pip.

```bash
pip install <package name> --index-url <package URL>
```

The URLs for repository can be quite long, so the wizard can be
used to generate the URLs based on the license key.
```bash
python library_wizard.py <package name> <key>
```

To also install the library, the optional install flag can be
set to "true".
```bash
python library_wizard.py <package name> <key> true
```

### Pip configuration

Ionworks python libraries can be installed from pyproject.toml and 
requirements.txt files by configuring pip to use extra index URLs.

Create a file named ```pip.conf``` and add the following lines:
```
[global]
index-url = <URL from library_wizard.py>
```

The pip configuration file needs to be exported as an environment
variable to take effect:
```bash
export PIP_CONFIG_FILE=pip.conf
```

Pip will then check for the libraries the Ionworks package servers
before checking PyPi.
