FROM 10.152.160.11:60919/gt-base/python-aigc:3.10-slim-bullseye-gt-aigc-20231117145038

ADD . ${BUILD_PREFIX}
ADD docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER noroot

ENTRYPOINT ["/entrypoint.sh"]
