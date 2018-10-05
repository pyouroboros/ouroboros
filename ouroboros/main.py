#!/usr/bin/env python3
import cli
import docker
import schedule
import time
import datetime
import logging
import container
import image
from logger import set_logger

def main():
    if not container.running():
        logging.info('No containers are running')
    else:
        updated_count = 0
        for running_container in container.to_monitor():
            current_image = cli.api_client.inspect_image(running_container['Config']['Image'])
            try:
                latest_image = image.pull_latest(current_image)
            except docker.errors.APIError as e:
                logging.error(e)
                continue
            # If current running container is running latest image
            if not image.is_up_to_date(current_image['Id'], latest_image['Id']):
                logging.info(('{} will be updated').format(container.get_name(running_container)))
                # new container object to create new container from
                new_config = container.NewContainerProperties(running_container, latest_image['RepoTags'][0])
                container.stop(running_container)
                container.remove(running_container)
                new_container = container.create_new_container(new_config.__dict__)
                container.start(new_container)
                image.remove(current_image)
                updated_count += 1
        logging.info('{} container(s) updated'.format(updated_count))

if __name__ == "__main__":
    cli.parser()
    set_logger(cli.debug)
    schedule.every(cli.interval).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(cli.interval - 5)
