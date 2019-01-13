![alt text](https://i.imgur.com/kYbI9Hi.png)

[![Travis](https://img.shields.io/travis/pyouroboros/ouroboros/master.svg?style=flat-square)](https://travis-ci.org/pyouroboros/ouroboros)
[![Discord](https://img.shields.io/badge/Discord-Ouroboros-7289DA.svg?logo=discord&style=flat-square)](https://discord.gg/qHNByUW)
[![BuyUsCoffee](https://img.shields.io/badge/BuyMeACoffee-Donate-ff813f.svg?logo=CoffeeScript&style=flat-square)](https://buymeacoff.ee/ouroboros)
[![Docker Pulls](https://img.shields.io/docker/pulls/pyouroboros/ouroboros.svg?style=flat-square)](https://hub.docker.com/r/pyouroboros/ouroboros/)
[![Layers](https://images.microbadger.com/badges/image/pyouroboros/ouroboros.svg)](https://microbadger.com/images/pyouroboros/ouroboros)
[![Image Version](https://images.microbadger.com/badges/version/pyouroboros/ouroboros.svg)](https://hub.docker.com/r/pyouroboros/ouroboros/)
[![Pypi Version](https://img.shields.io/pypi/v/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)

Automatically update your running Docker containers to the latest available image.

A python-based alternative to [watchtower](https://github.com/v2tec/watchtower)

## Table of Contents

- [Overview](#overview)
- [Changelog](doc/CHANGELOG.md)
- [Getting Started](#getting-started)
  - [Docker](#docker)
  - [Pip](#pip)
- [Examples](#examples)
  - [Monitor for updates for original tag](#monitor-for-updates-for-original-tag)
  - [Update containers on a remote host](#update-containers-on-a-remote-host)
  - [Change update frequency](#change-update-frequency)
  - [Change loglevel](#change-loglevel)
  - [Update all containers and quit ouroboros](#update-all-containers-and-quit-ouroboros)
  - [Remove old docker images](#remove-old-docker-images)
  - [Webhook Notifications](#webhook-notifications)
- [Prometheus metrics](#prometheus-metrics)
- [Contributing](#contributing)

## Overview

Ouroboros will monitor all running docker containers or those you specify and update said containers to the latest available image in the remote registry using the same tag and parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc.

- Push your image to your registry and simply wait a couple of minutes for ouroboros to find the new image and redeploy your container autonomously.
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs

## Getting Started

More detailed usage and configuration can be found on [the wiki](https://github.com/pyouroboros/ouroboros/wiki).

### Docker

Ouroboros is deployed via docker image like so:

**x86**
```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros
```

**Rpi 3 B+**
```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros:latest-aarch64-rpi
```

**All other Rpi's**
```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros:latest-arm-rpi
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
    image: pyouroboros/ouroboros
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

## Examples

### Monitor for updates for original tag
 Instead of always updating to `latest` you can specify if you would like Ouroboros to only check for updates for your original container's image tag.
 e.g. If your container was started with `nginx:1.14-alpine` using `--keep-tag` will poll the docker registry and compare digests. If there is a new image for `nginx:1.14-alpine`, ouroboros will update your container using the newly patched version.
 > Default is `False`
 ```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --keep-tag
```

### Update containers on a remote host

Ouroboros can monitor things other than just local, pass the `--url` argument to update a system with the Docker API exposed.

> Default is unix://var/run/docker.sock

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --url tcp://my-remote-docker-server:2375
```

### Change update frequency

An `interval` argument can be supplied to change how often ouroboros checks the remote docker registry for image updates (in seconds).

> Default is 300s

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --interval 600
```

### Monitor select containers

By default, ouroboros will monitor all running docker containers, but can be overridden to only monitor select containers by passing a `monitor` argument which supports an infinite amount of container names.

> Default is all

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --monitor container_1 container_2 container_3
```

### Change loglevel

The amount of logging details can be supressed by providing a `loglevel` argument.

> Default is info

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --loglevel debug
```

### Update all containers and quit ouroboros

If you prefer ouroboros didn't run all the time and only update all of your running containers in one go, provide the `runonce` argument and ouroboros will terminate itself after updating all your containers one time.

> Default is `False`

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --runonce
```

### Remove old docker images

Ouroboros has the option to remove the older docker image if a new one is found and the container is then updated. To tidy up after updates, pass the `cleanup` argument.

> Default is `False`

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --cleanup
```

### Prometheus metrics

Ouroboros keeps track of containers being updated and how many are being monitored. Said metrics are exported using [prometheus](https://prometheus.io/). Metrics are collected by ouroboros with or without this flag, it is up to you if you would like to expose the port or not. You can also bind the http server to a different interface for systems using multiple networks. `--metrics-port` and `--metrics-addr` can run independently of each other without issue.

#### Port

> Default is `8000`

```bash
 docker run -d --name ouroboros \	 ://my-webhook-1 https://my-webhook-2
   -p 5000:5000 \	 ://my-webhook-1 https://my-webhook-2
   -v /var/run/docker.sock:/var/run/docker.sock \	 ://my-webhook-1 https://my-webhook-2
   pyouroboros/ouroboros --metrics-port 5000	 ://my-webhook-1 https://my-webhook-2
 ```

You should then be able to see the metrics at http://localhost:5000/

#### Bind Address

Ouroboros allows you to bind the exporter to a different interface using the `--metrics-addr` argument. This works better for the CLI since docker networks always use `172.*.*.*` addresses, unless you have a very specific config.

> Default is `0.0.0.0`

```bash
docker run -d --name ouroboros \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --metrics-addr 10.0.0.1
```

Then access via http://10.0.0.1:8000/

**Example text from endpoint:**

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

### Webhook Notifications

See [notifications](#notifications)

 > Default is `None`

 ```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros --webhook-urls http://my-webhook-1 https://my-webhook-2
```

## Contributing

All welcome
