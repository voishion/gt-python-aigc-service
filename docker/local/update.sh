#!/bin/bash

usage() {
	echo "Usage: sh update.sh"
	exit 1
}
read -p "Enter need update container name: " name
containerName=$name
echo "Start update $containerName container"

# 关闭应用
docker stop $containerName
# 删除容器
docker container rm $containerName
# 删除镜像
docker images | grep $containerName | awk '{print $3}' | xargs docker rmi

# 重新构建部署
docker-compose up -d $containerName

echo "Update $containerName container success"
