# Container wizard

## Installation

The container installation wizard is used to run Docker images from
the ionworks package servers.

Script command:
```bash
python container_wizard.py <your_config_file>.yml
```
Command line alias:
```bash
ionwizard-container_wizard <your_config_file>.yml
```

Ionwizard will download the image, create a container, and start the
software. The image can be access here: http://localhost:8888/tree

### Docker

Ionwizard creates the containers using Docker. The Docker daemon needs to be
running to use the container wizard functionality.

### Configuration file

Containerized products licensed by ionworks can be directly installed by the 
container wizard. Each package requires a product name, version, and a license
key.
```yaml
docker:
  product: <Package name>
  version: <Version>
  key: <License key>
```
Only a single image can be specified in this configuration.

## Usage

### Loading data

Data can be loaded into the containers by using the following commands:
```bash
docker cp <path/to/your/data/directory> <container name>:/home/ionworks/data
```
The entire directory will then be copied to the container's data directory.
