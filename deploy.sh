#!/usr/bin/env bash
VERSION=$(grep -i version ouroboros/__init__.py | awk -F= '{gsub("\047",""); print $2}')
USER='circa10a'
PROJECT='ouroboros'
NAMESPACE=${USER}/${PROJECT}
# Auth
echo $docker_password | docker login -u=$USER --password-stdin
# Latest
docker build -t $NAMESPACE .
docker push $NAMESPACE
# Versioned
docker tag $NAMESPACE $NAMESPACE:$VERSION
docker push $NAMESPACE $NAMESPACE:$VERSION