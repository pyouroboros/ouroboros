#!/usr/bin/env bash
VERSION="$(grep -i version ./pyouroboros/__init__.py | awk -F= '{gsub("\047",""); gsub(",",""); print $2}')"

# Docker
GITHUB_USER='pyouroboros-bot'
DOCKER_USER='pyouroborosbot'
PROJECT='ouroboros'
NAMESPACE="pyouroboros/${PROJECT}"

# Docker experimental config
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
[ -d ~/.docker ] || mkdir ~/.docker
[ -f ~/.docker/config.json ] || touch ~/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee ~/.docker/config.json
sudo service docker restart

# Auth
echo $DOCKER_PASSWORD | docker login -u="$DOCKER_USER" --password-stdin

# Latest x64
docker build -t "${NAMESPACE}:latest" . && \
docker push "${NAMESPACE}:latest" && \
# Versioned x64
docker tag "${NAMESPACE}:latest" "${NAMESPACE}:${VERSION}" && \
docker push "${NAMESPACE}:${VERSION}" && \
# x64 Arch
docker tag "${NAMESPACE}:latest" "${NAMESPACE}:latest-amd64" && \
docker push "${NAMESPACE}:latest-amd64"

# Prepare qemu for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset

# ARM images
for i in $(ls *.rpi); do
  arch="$(echo ${i} | cut -d- -f2 | cut -d. -f1)"
  # Latest
  docker build -f "./Dockerfile-${arch}.rpi" -t "${NAMESPACE}:latest-${arch}-rpi" . && \
  docker push "${NAMESPACE}:latest-${arch}-rpi" && \
  # Versioned
  docker tag "${NAMESPACE}:latest-${arch}-rpi" "${NAMESPACE}:${VERSION}-${arch}-rpi" && \
  docker push "${NAMESPACE}:${VERSION}-${arch}-rpi"
done

wget -O manifest-tool https://github.com/estesp/manifest-tool/releases/download/v0.9.0/manifest-tool-linux-amd64 && \
chmod +x manifest-tool && \
./manifest-tool --username "$USER" --password "$docker_password" push from-spec "${USER}-${PROJECT}.yaml"
# Git tags
git remote set-url origin "https://${GITHUB_USER}:${GITHUB_API_KEY}@github.com/${NAMESPACE}.git" && \
git tag "${VERSION}" && \
git push --tags