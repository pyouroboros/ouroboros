#!/usr/bin/env python3
from sys import argv
from sys import exit
import time
import datetime
import logging
import docker
import schedule
import container
import image
import cli
from logger import set_logger
from prometheus_client import start_http_server
from prometheus_client import Counter


def main():
    """Find running containers and update them with images using latest tag"""
    log = logging.getLogger(__name__)
    # Setup our prometheus counter
    updated_containers_counter = Counter('containers_updated', 'Count of containers updated')
    if not container.running():
        log.info('No containers are running')
    else:
        updated_count = 0
        for running_container in container.to_monitor():
            current_image = cli.api_client.inspect_image(running_container['Config']['Image'])
            try:
                latest_image = image.pull_latest(image=current_image)
            except docker.errors.APIError as e:
                log.error(e)
                continue
            # If current running container is running latest image
            if not image.is_up_to_date(old_sha=current_image['Id'], new_sha=latest_image['Id']):
                log.info(f'{container.get_name(container_object=running_container)} will be updated')
                # new container dict to create new container from
                new_config = container.new_container_properties(old_container=running_container, new_image=latest_image['RepoTags'][0])
                container.stop(container_object=running_container)
                container.remove(container_object=running_container)
                new_container = container.create_new(config=new_config)
                container.start(container_object=new_container)
                if cli.cleanup:
                    image.remove(old_image=current_image)
                updated_count += 1
                updated_containers_counter.inc()

        log.info(f'{updated_count} container(s) updated')
        if cli.run_once:
            exit(0)


if __name__ == "__main__":
    cli.parser(argv[1:])
    # start our prometheus metrics http server
    if cli.metrics != 0:
        start_http_server(cli.metrics)
    logging.basicConfig(**set_logger(cli.loglevel))
    schedule.every(cli.interval).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
