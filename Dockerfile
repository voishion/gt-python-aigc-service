FROM 10.152.160.11:60919/gt-base/gt-python-aigc-service-base:231117

ADD . ${BUILD_PREFIX}

RUN cd ${BUILD_PREFIX} \
    && pip install --no-cache -r requirements.txt

ADD docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
USER noroot

ENTRYPOINT ["/entrypoint.sh"]
