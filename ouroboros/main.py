#!/usr/bin/env python3
import docker, schedule, time, datetime, logging,sys
import container, image, defaults
from logger import set_logger

client = docker.DockerClient(base_url=defaults.LOCAL_UNIX_SOCKET)
api_client = docker.APIClient(base_url=defaults.LOCAL_UNIX_SOCKET)

def main():
    if not container.running_properties():
        logging.info('No containers are running')
    else:
        for running_container in container.running_properties():
            current_image = client.images.get(running_container['ImageID'])
            try:
                latest_image = image.pull_latest(current_image)
            except docker.errors.APIError as e:
                logging.error(e)
                break
            # if current running container is running latest image
            if not image.is_up_to_date(current_image.id, latest_image.id):
                logging.info(('{} will be updated').format(container.get_name(running_container)))
                # new container object to create new container from
                new_config = container.NewContainerProperties(running_container, latest_image.tags[0])
                container.stop(running_container)
                container.remove(running_container)
                new_container = container.create_new_container(new_config.__dict__)
                container.start(new_container)
                image.remove(current_image.id)
        logging.info('All containers up to date')

if __name__ == "__main__":
    set_logger('debug')
    schedule.every(defaults.INTERVAL).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(defaults.INTERVAL / 5)
