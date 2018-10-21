#!/usr/bin/env bash -e
VERSION=$(grep -i version ouroboros/__init__.py | awk -F= '{gsub("\047",""); print $2}')

# Docker
USER='circa10a'
PROJECT='ouroboros'
NAMESPACE=${USER}/${PROJECT}
# Auth
echo $docker_password | docker login -u=$USER --password-stdin
# Latest
docker build -t $NAMESPACE:latest .
docker push $NAMESPACE:latest
# Versioned
docker tag $NAMESPACE:latest $NAMESPACE:$VERSION
docker push $NAMESPACE:$VERSION

# Git tags
git remote set-url origin https://$USER:$github_api_key@github.com/$USER/$PROJECT.git
git tag $VERSION
git push --tags