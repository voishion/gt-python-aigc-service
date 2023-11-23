FROM 10.152.160.11:60919/gt-base/python-aigc:3.10-slim-bullseye-gt-aigc-20231117145038

ADD . ${BUILD_PREFIX}
RUN chmod +x ${BUILD_PREFIX}/docker/entrypoint.sh

USER noroot

ENTRYPOINT ["/bin/sh", "-c", "${BUILD_PREFIX}/docker/entrypoint.sh"]