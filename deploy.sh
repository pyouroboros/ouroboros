#!/usr/bin/env bash
VERSION="$(grep -i version pyouroboros/__init__.py | cut -d' ' -f3 | tr -d \")"

# Docker
GITHUB_USER='pyouroboros-bot'
DOCKER_USER='pyouroborosbot'
PROJECT='ouroboros'
NAMESPACE="pyouroboros/${PROJECT}"

# Docker experimental config
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
[[ -d ~/.docker ]] || mkdir ~/.docker
[[ -f ~/.docker/config.json ]] || touch ~/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee ~/.docker/config.json
sudo service docker restart

# Auth
echo "$DOCKER_PASSWORD" | docker login -u="$DOCKER_USER" --password-stdin

# Latest x64
docker build -t "${NAMESPACE}:latest" . && \
docker push "${NAMESPACE}:latest" && \
# Versioned x64
docker tag "${NAMESPACE}:latest" "${NAMESPACE}:${VERSION}" && \
docker push "${NAMESPACE}:${VERSION}" && \
# x64 Arch
docker tag "${NAMESPACE}:latest" "${NAMESPACE}:latest-amd64" && \
docker push "${NAMESPACE}:latest-amd64"

# Prepare QEMU for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset
wget -P tmp/ "https://github.com/multiarch/qemu-user-static/releases/download/v3.1.0-2/qemu-aarch64-static"
wget -P tmp/ "https://github.com/multiarch/qemu-user-static/releases/download/v3.1.0-2/qemu-arm-static"
chmod +x tmp/qemu-aarch64-static tmp/qemu-arm-static

# ARM images
for i in $(ls *arm*); do
  arch="$(echo ${i} | cut -d. -f2)"
  # Latest
  docker build -f "./Dockerfile.${arch}" -t "${NAMESPACE}:latest-${arch}" . && \
  docker push "${NAMESPACE}:latest-${arch}" && \
  # Versioned
  docker tag "${NAMESPACE}:latest-${arch}" "${NAMESPACE}:${VERSION}-${arch}" && \
  docker push "${NAMESPACE}:${VERSION}-${arch}"
done

wget -O manifest-tool https://github.com/estesp/manifest-tool/releases/download/v0.9.0/manifest-tool-linux-amd64 && \
chmod +x manifest-tool && \
python3 manifest_generator.py && \
./manifest-tool --username "$USER" --password "$DOCKER_PASSWORD" push from-spec ".manifest.yaml"
# Git tags
git remote set-url origin "https://${GITHUB_USER}:${GITHUB_API_KEY}@github.com/${NAMESPACE}.git" && \
git tag "${VERSION}" && \
git push --tags