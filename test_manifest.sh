#!/usr/bin/env bash -e
VERSION=$(grep -i version ./setup.py | awk -F= '{gsub("\047",""); gsub(",",""); print $2}')

# Docker
USER='circa10a'
PROJECT='ouroboros'
NAMESPACE=${USER}/${PROJECT}
# Docker experimental config
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
[ -d ~/.docker ] || mkdir ~/.docker
[ -f ~/.docker/config.json ] || touch ~/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee ~/.docker/config.json
sudo service docker restart
# Auth
echo $docker_password | docker login -u=$USER --password-stdin

# Latest x86
docker build -t $NAMESPACE:latest . && \
docker push $NAMESPACE:latest && \
# Versioned x86
docker tag $NAMESPACE:latest $NAMESPACE:$VERSION && \
docker push $NAMESPACE:$VERSION

# prepare qemu for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset

for i in $(ls *.rpi); do
  arch="$(echo ${i} | cut -d- -f2 | cut -d. -f1)"
  # Latest
  docker build -f "./Dockerfile-${arch}.rpi" -t "$NAMESPACE:latest-${arch}-rpi" . && \
  docker push "$NAMESPACE:latest-${arch}-rpi" && \
  # Versioned
  docker tag "$NAMESPACE:latest-${arch}-rpi" "$NAMESPACE:${VERSION}-${arch}-rpi" && \
  docker push "$NAMESPACE:${VERSION}-${arch}-rpi"
done

# Support multiple architectures with same image
docker manifest create "${USER}/${PROJECT}:latest ${USER}/${PROJECT}:latest-aarch64-rpi"
docker manifest create "${USER}/${PROJECT}:latest ${USER}/${PROJECT}:latest-arm-rpi"
docker manifest annotate "${USER}/${PROJECT}:latest ${USER}/${PROJECT}:latest-aarch64-rpi --os linux --arch arm64 --variant armv8"
docker manifest annotate "${USER}/${PROJECT}:latest ${USER}/${PROJECT}:latest-arm-rpi --os linux --arch arm"
docker manifest push circa10a/ouroboros:latest
