#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /var/www/helloworld
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop helloworld
docker rm helloworld
docker rmi aprynur/helloworld
docker run -d --name helloworld -p 5000:5000 aprynur/helloworld:latest
