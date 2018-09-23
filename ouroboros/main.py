import docker
import containers, image
import datetime

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

def main():
    if not containers.running_properties():
        print('[INFO] {0:%Y-%m-%d %H:%M:%S} No containers are running'.format(datetime.datetime.now()))
    else:
        for running_container in containers.running_properties():
            current_image = client.images.get(running_container["ImageID"])
            try:
                latest_image = image.pull_latest(current_image)
            except docker.errors.APIError as e:
                print(e)
                break
            # if current running container is running latest image
            if not image.is_up_to_date(current_image.id, latest_image.id):
                print('[INFO] {0:%Y-%m-%d %H:%M:%S} {1} is out of date'.format(datetime.datetime.now(), str(running_container["Names"][0]).replace('/','')))
                # new container object to create new container from
                new_config = containers.NewContainerProperties(running_container, latest_image.tags[0])
                containers.stop(running_container)
                containers.remove(running_container)
                new_container = containers.create_new_container(new_config.__dict__)
                containers.start(new_container)
                image.remove(current_image.id)
        print('[INFO] {0:%Y-%m-%d %H:%M:%S} All containers up to date'.format(datetime.datetime.now()))

if __name__ == "__main__":
   main()