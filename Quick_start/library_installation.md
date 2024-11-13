# Library wizard

The library installation wizard is used to install python packages from
the ionworks package servers.

```bash
ionwizard-library -c <your_config_file>.yml
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
Setting the install flag to false will save the configuration file to disk
without installing the package.
