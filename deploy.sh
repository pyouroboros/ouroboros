#!/usr/bin/env bash
# Travis-ci convenience environment vars used:
# TRAVIS_BRANCH | branch name
# $TRAVIS_REPO_SLUG | organization/project (GitHub Capitalization)
# Travis-ci manual environment vars used:
# GITHUB_USER | github username
# GITHUB_TOKEN | $GITHUB_USER's token
# DOCKER_USER | docker username
# DOCKER_PASSWORD | $DOCKER_USER's password

VERSION="$(grep -i version pyouroboros/__init__.py | cut -d' ' -f3 | tr -d \")"

# Set branch to latest if master, else keep the same
if [[ "$TRAVIS_BRANCH" == "master" ]]; then
    BRANCH="latest"
else
    BRANCH="$TRAVIS_BRANCH"
fi

# get the docker lowercase variant of the repo_name
REPOSITORY="$(echo $TRAVIS_REPO_SLUG | tr '[:upper:]' '[:lower:]')"

# Docker experimental config
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
[[ -d ~/.docker ]] || mkdir ~/.docker
[[ -f ~/.docker/config.json ]] || touch ~/.docker/config.json
echo '{"experimental":"enabled"}' | sudo tee ~/.docker/config.json
sudo service docker restart

# Auth
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin

# Prepare QEMU for ARM builds
docker run --rm --privileged multiarch/qemu-user-static:register --reset
bash prebuild.sh
chmod +x qemu-aarch64-static qemu-arm-static

# Set tag based off of branch
if [[ "$BRANCH" == "latest" ]]; then
    TAG="$VERSION"
else
    TAG="$BRANCH"
fi

# AMDx64
docker build -t "${REPOSITORY}:${TAG}-amd64" . && \
docker push "${REPOSITORY}:${TAG}-amd64"

# Create Initial Manifests
docker manifest create "${REPOSITORY}:${TAG}" "${REPOSITORY}:${TAG}-amd64"
if [[ "$BRANCH" == "latest" ]]; then
    docker manifest create "${REPOSITORY}:${BRANCH}" "${REPOSITORY}:${TAG}-amd64"
fi

# ARM variants
for i in $(ls *arm*); do
    ARCH="$(echo ${i} | cut -d. -f2)"
    docker build -f "Dockerfile.${ARCH}" -t "${REPOSITORY}:${TAG}-${ARCH}" . && \
    docker push "${REPOSITORY}:${TAG}-${ARCH}"
    # Add variant to manifest
    docker manifest create -a "${REPOSITORY}:${TAG}" "${REPOSITORY}:${TAG}-${ARCH}"
    if [[ "$BRANCH" == "latest" ]]; then
        docker manifest create -a "${REPOSITORY}:${BRANCH}" "${REPOSITORY}:${TAG}-${ARCH}"
    fi
done

docker manifest inspect "${REPOSITORY}:${TAG}" && \
docker manifest push "${REPOSITORY}:${TAG}"
if [[ "$BRANCH" == "latest" ]]; then
    docker manifest inspect "${REPOSITORY}:${BRANCH}" && \
    docker manifest push "${REPOSITORY}:${BRANCH}"
fi

# Git tags
if [[ "$BRANCH" == "latest" ]]; then
    git remote set-url origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${REPOSITORY}.git" && \
    git tag "${VERSION}" && \
    git push --tags
fi