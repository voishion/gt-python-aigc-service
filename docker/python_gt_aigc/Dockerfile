FROM 10.152.160.83:60919/gt-base/python:3.10-slim-bullseye-gt

COPY requirements.txt ${BUILD_PREFIX}

RUN cd ${BUILD_PREFIX} \
    && pip install --no-cache -r requirements.txt \
    && rm -f requirements.txt



