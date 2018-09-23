#!/usr/bin/env python3
import docker, schedule, time, datetime, logging,sys
import containers, image
from logger import set_logger

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

def main():
    if not containers.running_properties():
        logging.info('No containers are running')
    else:
        for running_container in containers.running_properties():
            current_image = client.images.get(running_container["ImageID"])
            try:
                latest_image = image.pull_latest(current_image)
            except docker.errors.APIError as e:
                logging.error(e)
            # if current running container is running latest image
            if not image.is_up_to_date(current_image.id, latest_image.id):
                logging.info('{} will be updated').format(running_container["Names"][0].replace('/',''))
                # new container object to create new container from
                new_config = containers.NewContainerProperties(running_container, latest_image.tags[0])
                containers.stop(running_container)
                containers.remove(running_container)
                new_container = containers.create_new_container(new_config.__dict__)
                containers.start(new_container)
                image.remove(current_image.id)
        logging.info('All containers up to date')

if __name__ == "__main__":
    set_logger('debug')
    interval = 20
    schedule.every(interval).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(interval / 5)
