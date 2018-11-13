
![alt text](https://i.imgur.com/kYbI9Hi.png)

[![Travis](https://img.shields.io/travis/circa10a/ouroboros/master.svg?style=flat-square)](https://travis-ci.org/circa10a/ouroboros)
[![Codecov](https://img.shields.io/codecov/c/github/circa10a/ouroboros.svg?style=flat-square)](https://codecov.io/gh/circa10a/ouroboros)
[![Docker Pulls](https://img.shields.io/docker/pulls/circa10a/ouroboros.svg?style=flat-square)](https://hub.docker.com/r/circa10a/ouroboros/)
[![Layers](https://images.microbadger.com/badges/image/circa10a/ouroboros.svg)](https://microbadger.com/images/circa10a/ouroboros)
[![Image Version](https://images.microbadger.com/badges/version/circa10a/ouroboros.svg)](https://hub.docker.com/r/circa10a/ouroboros/)
[![Pypi Version](https://img.shields.io/pypi/v/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)

Automatically update your running Docker containers to the latest available image.

A python-based alternative to [watchtower](https://github.com/v2tec/watchtower)

## Overview

Ouroboros will monitor all running docker containers or those you specify and update said containers to the latest available image in the remote registry using the `latest` tag with the same parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc. While ouroboros updates images to `latest` by default, that can be [overridden](#Options) to only monitor updates of a specific tag. Similar to [watchtower](https://github.com/v2tec/watchtower).

- Push your image to your registry and simply wait a couple of minutes for ouroboros to find the new image and redeploy your container autonomously.
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs

## Usage
![alt text](https://thumbs.gfycat.com/SerpentineExhaustedHind-size_restricted.gif)

### Docker

Ouroboros is deployed via docker image like so:

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
```

or via `docker-compose`:

```yaml
version: '3'
services:
  nginx:
    image: nginx:1.14-alpine
    ports:
     - 80:80
  ouroboros:
    image: circa10a/ouroboros
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 60 --loglevel debug
```

### Pip
Ouroboros can also be installed via `pip`:

```bash
pip install ouroboros-cli
```

And can then be invoked using the `ouroboros` command:

```bash
$ ouroboros --interval 5 --loglevel debug
```

> This can be useful if you would like to create a `systemd` service or similar daemon that doesn't run in a container

### Options

> All arguments can be ran together without conflication

> All arguments can be supplemented with environment variables, but command line arguments will take priority

```
docker run --rm circa10a/ouroboros --help
```

- `--url`, `-u` Monitor and update containers on a remote system by providing the `url` argument.
  - Default is `unix://var/run/docker.sock`.
  - Environment variable: `URL=tcp://localhost:2375`.
- `--interval`, `-i` Change how often ouroboros checks the remote docker registry for image updates (in seconds).
  - Default is `300`.
  - Environment variable: `INTERVAL=60`.
- `--monitor`, `-m` Only monitor select containers which supports an infinite amount of container names.
  - Default is all containers.
  - Environment variable: `MONITOR=test_container`
- `--ignore`, `-n` Ignore the listed container names.
  - Default is none.
  - Environment variable: `IGNORE=test_container`
  - If a container name is specified to monitor and ignore, ignore takes precedent.
- `--loglevel`, `-l` The amount of logging details can be supressed or increased.
  - Default is `info`.
  - Environment variable: `LOGLEVEL=debug`.
- `--runonce`, `-r` Update all your running containers in one go and terminate ouroboros.
  - Default is `False`.
  - Environment variable: `RUNONCE=true`.
- `--cleanup`, `-c` Remove the older docker image if a new one is found and updated.
  - Default is `False`.
  - Environment variable: `CLEANUP=true`
- `--keep-tag`, `-k` Only monitor if updates are made to the tag of the image that the container was created with instead of using `latest`.
  - Default is `False`.
  - Environment variable: `KEEPTAG=true`
- `--metrics` What port to run prometheus endpoint on. Running on port `8000` by default if `--metrics` is not supplied.
  - Default is `8000`.
  - Environment variable: `METRICS`

### Private Registries

If your running containers' docker images are stored in a secure registry that requires a username and password, simply run ouroboros with 2 environment variables(`REPO_USER` and `REPO_PASS`).

```bash
docker run -d --name ouroboros \
  -v REPO_USER=myUser -e REPO_PASS=myPassword \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
```

You can alternatively bind mount `~/.docker/config.json` which won't require the above environment variables.

```bash
docker run -d --name ouroboros \
  -v $HOME/.docker/config.json:/root/.docker/config.json \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
```

## Examples

### Monitor for updates for original tag
 Instead of always updating to `latest` you can specify if you would like Ouroboros to only check for updates for your original container's image tag.
 e.g. If your container was started with `nginx:1.14-alpine` using `--keep-tag` will poll the docker registry and compare digests. If there is a new image for `nginx:1.14-alpine`, ouroboros will update your container using the newly patched version.
 > Default is `False`
 ```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --keep-tag
```

### Update containers on a remote host

Ouroboros can monitor things other than just local, pass the `--url` argument to update a system with the Docker API exposed.

> Default is unix://var/run/docker.sock

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --url tcp://my-remote-docker-server:2375
```

### Change update frequency

An `interval` argument can be supplied to change how often ouroboros checks the remote docker registry for image updates (in seconds).

> Default is 300s

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --interval 600
```

### Monitor select containers

By default, ouroboros will monitor all running docker containers, but can be overridden to only monitor select containers by passing a `monitor` argument which supports an infinite amount of container names.

> Default is all

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --monitor containerA containerB containerC
```

### Change loglevel

The amount of logging details can be supressed by providing a `loglevel` argument.

> Default is info

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --loglevel debug
```

### Update all containers and quit ouroboros

If you prefer ouroboros didn't run all the time and only update all of your running containers in one go, provide the `runonce` argument and ouroboros will terminate itself after updating all your containers one time.

> Default is `False`

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --runonce
```

### Remove old docker images

Ouroboros has the option to remove the older docker image if a new one is found and the container is then updated. To tidy up after updates, pass the `cleanup` argument.

> Default is `False`

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --cleanup
```

### Prometheus metrics

Ouroboros keeps track of containers being updated and how many are being monitored. Said metrics are exported using `prometheus`. Metrics are enabled with or without this flag, it is up to you if you would like to expose the port or not.

> Default is `8000`

```bash
docker run -d --name ouroboros \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --metrics 5000
```

You should then be able to see the metrics at http://localhost:5000/

Example text from endpoint:

```
# HELP containers_updated_total Count of containers updated
# TYPE containers_updated_total counter
containers_updated_total{container="all"} 2.0
containers_updated_total{container="alpine"} 1.0
containers_updated_total{container="busybox"} 1.0
# TYPE containers_updated_created gauge
containers_updated_created{container="all"} 1542152615.625264
containers_updated_created{container="alpine"} 1542152615.6252713
containers_updated_created{container="busybox"} 1542152627.7476819
# HELP containers_being_monitored Count of containers being monitored
# TYPE containers_being_monitored gauge
containers_being_monitored 2.0
```

## Execute Tests

> Script will install dependencies from `requirements-dev.txt`

All tests:

```bash
./run_tests.sh
```

Unit tests:

```bash
./run_tests.sh unit
```

Integration tests:

```bash
./run_tests.sh integration
```

## Contributing

All welcome
