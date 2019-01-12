#!/usr/bin/env bash -e
VERSION=$(grep -i version ./setup.py | awk -F= '{gsub("\047",""); gsub(",",""); print $2}')

# Docker
USER='pyouroboros'
PROJECT='ouroboros'
NAMESPACE=${USER}/${PROJECT}
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

# Git tags
git remote set-url origin "https://${USER}:${github_api_key}@github.com/${USER}/${PROJECT}.git" && \
git tag "$VERSION" && \
git push --tags