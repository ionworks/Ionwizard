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
ionwizard-container <your_config_file>.yml
```

Ionwizard will download the image, create a container, and start the
software. The image can be access here: http://localhost:8888/tree

## System requirements

### Docker

Ionwizard creates and runs containerized versions of ionworks software using 
[Docker]. Docker needs to be running in the background in order to use an 
ionworks container.

## Troubleshooting

General:
- Curl is required to fetch the Docker image. While curl should be installed 
  on most systems. Older operating systems might require a manual install.
- Docker must be installed and running to use the containers.

MacOS:
- The [Rosetta] compatibility library is needed to get good 
  performance with Docker on systems using Apple Silicon.
- To use Rosetta with Docker, open Docker Desktop and go to settings, then
  check the box "Use Rosetta for x86_64/amd64 emulation on Apple Silicon". 
  This may require updating to the newest version of Docker.

### Configuration file

Containerized products licensed by ionworks can be directly installed by the 
container wizard. Each package requires a product name, version, and a license
key.
```yaml
docker:
  product: <Package name>
  version: <Version>
  key: <License key>
  restart: False
```
Only a single image can be specified in this configuration.

## Usage

### Restarting a container

If a container has been used already then it can be restarted by updating the
restart value in the configuration file:
```yaml
docker:
  product: <Package name>
  version: <Version>
  key: <License key>
  restart: True
```
Setting restart to `True` will skip the download of a new container and 
restart the existing one instead. This will preserve any data, notebooks, or 
files created inside the container.

### Loading data

Data can be loaded into the containers by using the following commands:
```bash
docker cp <path/to/your/data/directory> <container name>:/home/ionworks/data
```
The entire directory will then be copied to the container's data directory.


[Docker]: https://www.docker.com/products/docker-desktop/
[Rosetta]: https://developer.apple.com/documentation/apple-silicon/about-the-rosetta-translation-environment