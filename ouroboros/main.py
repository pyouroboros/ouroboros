#!/usr/bin/env python3
import cli
import docker
import schedule
import time
import datetime
import logging
import container
import image
from sys import argv
from logger import set_logger

def main():
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
                new_config = container.NewContainerProperties(running_container, latest_image['RepoTags'][0])
                container.stop(running_container)
                container.remove(running_container)
                new_container = container.create_new(vars(new_config))
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
