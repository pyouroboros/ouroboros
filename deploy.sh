#!/usr/bin/env bash -e
VERSION=$(grep -i version ./setup.py | awk -F= '{gsub("\047",""); gsub(",",""); print $2}')

# Docker
USER='circa10a'
PROJECT='ouroboros'
NAMESPACE=${USER}/${PROJECT}
# Auth
echo $docker_password | docker login -u=$USER --password-stdin

# Latest x86
docker build -t $NAMESPACE:latest .
docker push $NAMESPACE:latest
# Versioned x86
docker tag $NAMESPACE:latest $NAMESPACE:$VERSION
docker push $NAMESPACE:$VERSION

# prepare qemu for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset

# Latest ARM
docker build -f ./Dockerfile.rpi -t $NAMESPACE:latest-rpi .
docker push $NAMESPACE:latest-rpi
# Versioned ARM
docker tag $NAMESPACE:latest-rpi $NAMESPACE:$VERSION-rpi
docker push $NAMESPACE:$VERSION-rpi

# Git tags
git remote set-url origin https://$USER:$github_api_key@github.com/$USER/$PROJECT.git
git tag $VERSION
git push --tags