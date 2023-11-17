FROM python:3.10-slim-bullseye

LABEL maintainer="lilu1@hydsoft.com"
ENV TZ='Asia/Shanghai'

RUN echo /etc/apt/sources.list
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
ENV BUILD_PREFIX=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash \
    && mkdir ${BUILD_PREFIX} \
    && cd ${BUILD_PREFIX} \
    && /usr/local/bin/python -m pip install --no-cache --upgrade pip

WORKDIR ${BUILD_PREFIX}

RUN mkdir -p /home/noroot \
    && groupadd -r noroot \
    && useradd -r -g noroot -s /bin/bash -d /home/noroot noroot \
    && chown -R noroot:noroot /home/noroot ${BUILD_PREFIX} /usr/local/lib

USER noroot
