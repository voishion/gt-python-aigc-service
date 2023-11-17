FROM python:3.10-slim-bullseye

LABEL maintainer="lilu1@hydsoft.com"

ENV TZ='Asia/Shanghai'
ENV BUILD_PREFIX=/app

RUN echo /etc/apt/sources.list \
    && sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends bash \
    && mkdir ${BUILD_PREFIX} \
    && cd ${BUILD_PREFIX} \
    && /usr/local/bin/python -m pip install --no-cache --upgrade pip

WORKDIR ${BUILD_PREFIX}

RUN mkdir -p /home/noroot \
    && groupadd -r noroot \
    && useradd -r -g noroot -s /bin/bash -d /home/noroot noroot \
    && chown -R noroot:noroot /home/noroot ${BUILD_PREFIX} /usr/local/lib
