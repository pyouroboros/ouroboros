import docker
import containers, image

client = docker.from_env()

def main():
    for container in containers.running():
        print(image.pull_latest(container.image).id)
        print(image.pull_latest(container.image).tags[0])

if __name__ == "__main__":
    main()