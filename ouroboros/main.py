import docker
import containers, image

client = docker.from_env()

def main():
    for running_container in containers.running_properties():
        current_image = client.images.get(running_container["ImageID"])
        latest_image = image.pull_latest(current_image)
        # if current running container is running latest image
        #print(current_image.id == latest_image.id)
        # new container object to create new container from
        print(containers.new_container_properties(running_container, latest_image.tags[0]).__dict__)
if __name__ == "__main__":
    main()