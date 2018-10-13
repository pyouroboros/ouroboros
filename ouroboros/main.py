#!/usr/bin/env python3
from sys import argv
import time
import datetime
import logging
import docker
import schedule
import container
import image
import cli
from logger import set_logger

def main():
    """Find running containers and update them with images using latest tag"""
    log = logging.getLogger(__name__)
    if not container.running():
        log.info('No containers are running')
    else:
        updated_count = 0
        for running_container in container.to_monitor():
            current_image = cli.api_client.inspect_image(running_container['Config']['Image'])
            try:
                latest_image = image.pull_latest(current_image)
            except docker.errors.APIError as e:
                log.error(e)
                continue
            # If current running container is running latest image
            if not image.is_up_to_date(current_image['Id'], latest_image['Id']):
                log.info(f'{container.get_name(running_container)} will be updated')
                # new container object to create new container from
                new_config = container.new_container_properties(running_container, latest_image['RepoTags'][0])
                container.stop(running_container)
                container.remove(running_container)
                new_container = container.create_new(new_config)
                container.start(new_container)
                image.remove(current_image)
                updated_count += 1
        log.info(f'{updated_count} container(s) updated')

if __name__ == "__main__":
    cli.parser(argv[1:])
    logging.basicConfig(**set_logger(cli.level))
    schedule.every(cli.interval).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(cli.interval - 5)
