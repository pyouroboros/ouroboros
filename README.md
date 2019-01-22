<img width="800" src="https://bin.cajun.pro/images/ouroboros/ouroboros_logo_primary_long_cropped.jpg">

[![Discord](https://img.shields.io/discord/532695326117593112.svg?colorB=7289DA&label=Discord&logo=Discord&logoColor=7289DA&style=flat-square)](https://discord.gg/qHNByUW)
[![BuyUsCoffee](https://img.shields.io/badge/BuyMeACoffee-Donate-ff813f.svg?logo=CoffeeScript&style=flat-square)](https://buymeacoff.ee/ouroboros)  
[![Travis](https://img.shields.io/travis/pyouroboros/ouroboros/master.svg?style=flat-square)](https://travis-ci.org/pyouroboros/ouroboros)
[![Release](https://img.shields.io/github/release/pyouroboros/ouroboros.svg?style=flat-square)](https://hub.docker.com/r/pyouroboros/ouroboros/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)
[![Python Version](https://img.shields.io/pypi/pyversions/ouroboros-cli.svg?style=flat-square)](https://pypi.org/project/ouroboros-cli/)
[![Docker Pulls](https://img.shields.io/docker/pulls/pyouroboros/ouroboros.svg?style=flat-square)](https://hub.docker.com/r/pyouroboros/ouroboros/)
[![Layers](https://images.microbadger.com/badges/image/pyouroboros/ouroboros.svg)](https://microbadger.com/images/pyouroboros/ouroboros)
Automatically update your running Docker containers to the latest available image.

A python-based alternative to [watchtower](https://github.com/v2tec/watchtower)

## Overview

Ouroboros will monitor (all or specified) running docker containers and update them to the (latest or tagged) available image in the remote registry. The updated container uses the same tag and parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc.

- Push your image to your registry and simply wait your defined interval for ouroboros to find the new image and redeploy your container autonomously.
- Notify you via email or platform customized webhooks. (Currently: Discord/Slack/Pushover/HealthChecks/Generic)
- Serve metrics for trend monitoring (Currently: Prometheus/Influxdb)
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs
- `docker-compose pull && docker-compose up -d` is for fancier scrubs

## Getting Started

More detailed usage and configuration can be found on [the wiki](https://github.com/pyouroboros/ouroboros/wiki).

### Docker

Ouroboros is deployed via docker image like so:

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  pyouroboros/ouroboros
```

> This is image is compatible for amd64, arm32, and arm64 CPU architectures

or via `docker-compose`:

[Official Example](https://github.com/pyouroboros/ouroboros/blob/master/docker-compose.yml)

### Pip

Ouroboros can also be installed via `pip`:

```bash
pip install ouroboros-cli
```

And can then be invoked using the `ouroboros` command:

```bash
$ ouroboros --interval 300 --loglevel debug
```

> This can be useful if you would like to create a `systemd` service or similar daemon that doesn't run in a container

## Examples

### Monitor for updates for latest tag
 Instead of updating to your original image tag you can specify if you would like Ouroboros to update all containers to `latest`.  
 e.g. If your container was started with `nginx:1.14-alpine` using `LATEST=true` will poll the docker registry and compare digests. If there is a new image for `nginx:latest`, ouroboros will update your container using the newly patched version.
 > Default is `false`
 ```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e LATEST=true \
  pyouroboros/ouroboros
```

### Update containers on a remote host

Ouroboros can monitor things other than just local, pass the `--docker-sockets` argument to update a system with the Docker API exposed or alternatively pass the `DOCKER_SOCKETS` environment variable.

> Default is unix://var/run/docker.sock

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKER_SOCKETS=tcp://my-remote-docker-server:2376 \
  pyouroboros/ouroboros
```

Many more examples are located in our wiki on the [usage page](https://github.com/pyouroboros/ouroboros/wiki/Usage)

## Contributing

All welcome
