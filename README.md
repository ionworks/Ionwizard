# Ionworks Installation Wizard

Ionworks products are stored on private repositories. The software in
this project is designed to help users access ionworks software.

## Python libraries

The Python packages produced by ionworks can be installed via pip.
The ionworks packages are stored on a private server, but can be
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

## Container images

Some ionworks software is delivered as pre-configured containers.
```

```