#!/bin/bash

docker logout
docker login 10.152.160.83:60919

latest_ver=3.10-slim-bullseye-gt-aigc-$(date +"%Y%m%d%H%M%S")
images_name=10.152.160.83:60919/gt-base/python-aigc

cp ../../requirements.txt ./

echo "images info:$images_name"

echo "build images..."
docker build -f Dockerfile -t $images_name .

echo "images version:$latest_ver"

echo "images tag..."
docker tag $images_name $images_name:"$latest_ver"

echo "images push..."
docker push $images_name:"$latest_ver"

docker logout

rm -f requirements.txt