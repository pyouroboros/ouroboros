from sys import exit
import logging
import docker
from ouroboros import container
from ouroboros import image
from ouroboros import metrics


def main(args, api_client):
    """Find running containers and update them with images using latest tag"""
    log = logging.getLogger(__name__)
    if not container.running(api_client=api_client):
        log.info('No containers are running')
    else:
        updated_count = 0
        monitored_containers = container.to_monitor(monitor=args.monitor, ignore=args.ignore, api_client=api_client)
        metrics.monitored_containers(num=len(monitored_containers))
        for running_container in monitored_containers:
            container_name = f'{container.get_name(container_object=running_container)}'
            current_image = api_client.inspect_image(running_container['Config']['Image'])

            try:
                latest_image = image.pull_latest(image=current_image, keep_tag=args.keep_tag, api_client=api_client)
            except docker.errors.APIError as e:
                log.error(e)
                continue

            # If current running container is running latest image
            if not image.is_up_to_date(old_sha=current_image['Id'], new_sha=latest_image['Id']):
                log.info(f'{container.get_name(container_object=running_container)} will be updated')

                # new container dict to create new container from
                new_config = container.new_container_properties(old_container=running_container,
                                                                new_image=latest_image['RepoTags'][0])

                container.stop(container_object=running_container, api_client=api_client)

                container.remove(container_object=running_container, api_client=api_client)

                new_container = container.create_new(config=new_config, api_client=api_client)

                container.start(container_object=new_container, api_client=api_client)

                if args.cleanup:
                    image.remove(old_image=current_image, api_client=api_client)
                updated_count += 1

                metrics.container_updates(label='all')
                metrics.container_updates(label=container_name)

        log.info(f'{updated_count} container(s) updated')
        if args.run_once:
            exit(0)
