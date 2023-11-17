#!/bin/bash

docker logout

latest_ver=3.10-slim-bullseye-gt
images_name=10.152.160.83:60919/gt-base/python

echo "images info:$images_name"

echo "build images..."
docker build -f Dockerfile -t $images_name .

echo "images version:$latest_ver"

echo "images tag..."
docker tag $images_name $images_name:"$latest_ver"

docker logout
docker login 10.152.160.83:60919

echo "images push..."
docker push $images_name:"$latest_ver"

docker logout