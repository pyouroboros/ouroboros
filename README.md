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

## Table of Contents

- [Overview](#overview)
- [Changelog](doc/CHANGELOG.md)
- [Usage](#usage)
  - [Docker](#docker)
  - [Pip](#pip)
  - [Options](#options)
  - [Config File](#config-file)
  - [Private Registries](#private-registries)
  - [Scheduling](#scheduling)
  - [Timezone Configuration](#timezone-configuration)
  - [Notifications](#notifications)
- [Examples](#examples)
  - [Monitor for updates for original tag](#monitor-for-updates-for-original-tag)
  - [Update containers on a remote host](#update-containers-on-a-remote-host)
  - [Change update frequency](#change-update-frequency)
  - [Change loglevel](#change-loglevel)
  - [Update all containers and quit ouroboros](#update-all-containers-and-quit-ouroboros)
  - [Remove old docker images](#remove-old-docker-images)
  - [Webhook Notifications](#webhook-notifications)
- [Prometheus metrics](#prometheus-metrics)
- [Execute Tests](#execute-tests)
- [Contributing](#contributing)

## Overview

pyouroboros will monitor all running docker containers or those you specify and update said containers to the latest available image in the remote registry using the `latest` tag with the same parameters that were used when the container was first created such as volume/bind mounts, docker network connections, environment variables, restart policies, entrypoints, commands, etc. While ouroboros updates images to `latest` by default, that can be [overridden](#Options) to only monitor updates of a specific tag. Similar to [watchtower](https://github.com/v2tec/watchtower).

- Push your image to your registry and simply wait a couple of minutes for ouroboros to find the new image and redeploy your container autonomously.
- Limit your server ssh access
- `ssh -i key server.domainname "docker pull ... && docker run ..."` is for scrubs

## Usage
![alt text](https://thumbs.gfycat.com/SerpentineExhaustedHind-size_restricted.gif)

### Docker

pyouroboros is deployed via docker image like so:

**x86**
```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
```

**ARM/RPI**
```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros:latest-rpi
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
pyouroboros can also be installed via `pip`:

```bash
pip install ouroboros-cli
```

And can then be invoked using the `ouroboros` command:

```bash
$ ouroboros --interval 5 --loglevel debug
```

> This can be useful if you would like to create a `systemd` service or similar daemon that doesn't run in a container

### Options

> All arguments can be ran together without confliction

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
  - Environment variable: `MONITOR=container_1`
- `--ignore`, `-n` Ignore the listed container names.
  - Default is none.
  - Environment variable: `IGNORE=container_1`
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
- `--keep-tag`, `-k` Only monitor if updates are made to the tag of the image that the container was created with instead of using `latest`. This will enable [watchtower](https://github.com/v2tec/watchtower)-like functionality.
  - Default is `False`.
  - Environment variable: `KEEPTAG=true`
- `--metrics-addr` What address for the prometheus endpoint to bind to. This arg is best suited for `ouroboros-cli`.
  - Default is `0.0.0.0`.
  - Environment variable: `METRICS_ADDR=0.0.0.0`
- `--metrics-port` What port to run prometheus endpoint on. Running on port `8000` by default if `--metrics-port` is not supplied.
  - Default is `8000`.
  - Environment variable: `METRICS_PORT=8000`
- `-w, --webhook-urls` What URLs for ouroboros to POST when a container is updated.
  - Default is `None`.
  - Environment variable: `WEBHOOK_URLS=http://my-webhook-1`

### Config File

You can provide a [docker env file](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) to supplement a config file with all the above listed arguments by utilizing the supported environment variables.

```bash
docker run -d --name ouroboros \
  --env-file env.list \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
```

**Sample env.list**

```
URL=tcp://localhost:2375
INTERVAL=60
KEEPTAG=true
MONITOR='["container_1", "container_2"]'
```
### Private Registries

If your running containers' docker images are stored in a secure registry that requires a username and password, simply run ouroboros with 2 environment variables(`REPO_USER` and `REPO_PASS`).

```bash
docker run -d --name ouroboros \
  -e REPO_USER=myUser -e REPO_PASS=myPassword \
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
### Scheduling

pyouroboros does not have a native scheduling implementation other than using `--interval`. This is due to there being more robust/customizable job schedulers being available such as:

- Cron
  - [Cron Tutorial](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/)
  - [Cron Expression Creator](https://crontab.guru/)
- Systemd Timers
  - [Documentation](https://wiki.archlinux.org/index.php/Systemd/Timers)

Example using ouroboros to update containers every Monday at 5AM:

**Docker**

```bash
* 5 * * 1 docker run --rm -d --name ouroboros -v /var/run/docker.sock:/var/run/docker.sock circa10a/ouroboros --interval 1 --runonce
```

**Pip installed CLI**

```bash
* 5 * * 1 ouroboros --interval 1 --runonce
```

Using the [`--runonce`](#update-all-containers-and-quit-ouroboros) arg tells ouroboros to make one pass updating all/specified containers and then exit.

### Timezone Configuration

To more closely monitor ouroboros' actions and for accurate log ingestion, you can change the timezone of the container from UTC by setting the [`TZ`](http://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html) environment variable like so:

```
docker run -d --name ouroboros \
  -e TZ=America/Chicago \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros
  ```

## Notifications

### Webhooks

Ourboros has the ability to trigger multiple webhooks for slack integration or other automation. Detailed request information can be seen by [enabling the debug loglevel](#change-loglevel). If the appropriate [args/environment variables](#options) are supplied, a POST request will be sent to specified URLs with a slack-compatible JSON payload like so:


```
{"text": "Container: alpine updated from sha256:34ea7509dcad10aa92310f2b41e3afbabed0811ee3a902d6d49cb90f075fe444 to sha256:3f53bb00af943dfdf815650be70c0fa7b426e56a66f5e3362b47a129d57d5991"}
```

## Examples

### Monitor for updates for original tag
 Instead of always updating to `latest` you can specify if you would like pyouroboros to only check for updates for your original container's image tag.
 e.g. If your container was started with `nginx:1.14-alpine` using `--keep-tag` will poll the docker registry and compare digests. If there is a new image for `nginx:1.14-alpine`, ouroboros will update your container using the newly patched version.
 > Default is `False`
 ```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --keep-tag
```

### Update containers on a remote host

pyouroboros can monitor things other than just local, pass the `--url` argument to update a system with the Docker API exposed.

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
  circa10a/ouroboros --monitor container_1 container_2 container_3
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

pyouroboros has the option to remove the older docker image if a new one is found and the container is then updated. To tidy up after updates, pass the `cleanup` argument.

> Default is `False`

```bash
docker run -d --name ouroboros \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --cleanup
```

### Prometheus metrics

pyouroboros keeps track of containers being updated and how many are being monitored. Said metrics are exported using [prometheus](https://prometheus.io/). Metrics are collected by ouroboros with or without this flag, it is up to you if you would like to expose the port or not. You can also bind the http server to a different interface for systems using multiple networks. `--metrics-port` and `--metrics-addr` can run independently of each other without issue.

#### Port

> Default is `8000`

```bash
 docker run -d --name ouroboros \	 ://my-webhook-1 https://my-webhook-2
   -p 5000:5000 \	 ://my-webhook-1 https://my-webhook-2
   -v /var/run/docker.sock:/var/run/docker.sock \	 ://my-webhook-1 https://my-webhook-2
   circa10a/ouroboros --metrics-port 5000	 ://my-webhook-1 https://my-webhook-2
 ```

You should then be able to see the metrics at http://localhost:5000/

#### Bind Address

pyouroboros allows you to bind the exporter to a different interface using the `--metrics-addr` argument. This works better for the CLI since docker networks always use `172.*.*.*` addresses, unless you have a very specific config.

> Default is `0.0.0.0`

```bash
docker run -d --name ouroboros \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  circa10a/ouroboros --metrics-addr 10.0.0.1
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
  circa10a/ouroboros --webhook-urls http://my-webhook-1 https://my-webhook-2
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
