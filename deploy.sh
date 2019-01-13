#!/usr/bin/env bash -e
VERSION=$(grep -i version ./setup.py | awk -F= '{gsub("\047",""); gsub(",",""); print $2}')

# Docker
GITHUB_USER='pyouroboros-bot'
DOCKER_USER='pyouroborosbot'
PROJECT='ouroboros'
NAMESPACE="pyouroboros/${PROJECT}"
# Auth
echo $DOCKER_PASSWORD | docker login -u="$DOCKER_USER" --password-stdin

# Latest x86
docker build -t $NAMESPACE:latest . && \
docker push $NAMESPACE:latest && \
# Versioned x86
docker tag $NAMESPACE:latest $NAMESPACE:$VERSION && \
docker push $NAMESPACE:$VERSION

# prepare qemu for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset

for i in $(ls *.rpi); do
  ARCH="$(echo ${i} | cut -d- -f2 | cut -d. -f1)"
  # Latest
  docker build -f "./Dockerfile-${ARCH}.rpi" -t "${NAMESPACE}:latest-${ARCH}-rpi" . && \
  docker push "${NAMESPACE}:latest-${ARCH}-rpi" && \
  # Versioned
  docker tag "${NAMESPACE}:latest-${ARCH}-rpi" "${NAMESPACE}:${VERSION}-${ARCH}-rpi" && \
  docker push "${NAMESPACE}:${VERSION}-${ARCH}-rpi"
done

# Git tags
git remote set-url origin "https://${GITHUB_USER}:${GITHUB_API_KEY}@github.com/${NAMESPACE}.git" && \
git tag "${VERSION}" && \
git push --tags