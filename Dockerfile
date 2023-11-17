FROM python:3.10-slim-bullseye

LABEL maintainer="lilu1@hydsoft.com"
ARG TZ='Asia/Shanghai'

RUN echo /etc/apt/sources.list
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
ENV BUILD_PREFIX=/app

ADD . ${BUILD_PREFIX}

RUN apt-get update \
    &&apt-get install -y --no-install-recommends bash\
    && cd ${BUILD_PREFIX} \
    && /usr/local/bin/python -m pip install --no-cache --upgrade pip \
    && pip install --no-cache -r requirements.txt

WORKDIR ${BUILD_PREFIX}

ADD docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && mkdir -p /home/noroot \
    && groupadd -r noroot \
    && useradd -r -g noroot -s /bin/bash -d /home/noroot noroot \
    && chown -R noroot:noroot /home/noroot ${BUILD_PREFIX} /usr/local/lib

USER noroot

ENTRYPOINT ["/entrypoint.sh"]
