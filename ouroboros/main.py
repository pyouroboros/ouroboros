import docker
import containers, image

client = docker.from_env()

def main():
    for container in containers.running():
        print(image.pull_latest(container.image))

if __name__ == "__main__":
    main()