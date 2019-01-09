#!/usr/bin/env bash
echo '{"experimental":true}' | sudo tee /etc/docker/daemon.json
sudo service docker restart
docker manifest create circa10a/ouroboros:latest circa10a/ouroboros:amd64-latest circa10a/ouroboros:arm32v6-latest circa10a/ouroboros:arm64v8-latest
docker manifest annotate circa10a/ouroboros:latest circa10a/ouroboros:arm32v6-latest --os linux --arch arm
docker manifest annotate circa10a/ouroboros:latest circa10a/ouroboros:arm64v8-latest --os linux --arch arm64 --variant armv8
docker manifest push circa10a/ouroboros:latest