#!/bin/bash
set -e

# build prefix
AIGC_SERVICE_PREFIX=${AIGC_SERVICE_PREFIX:-""}
# execution command line
AIGC_SERVICE_EXEC=${AIGC_SERVICE_EXEC:-""}

# use environment variables to pass parameters
# if you have not defined environment variables, set them below
# export OPEN_AI_API_KEY=${OPEN_AI_API_KEY:-'YOUR API KEY'}

# AIGC_SERVICE_PREFIX is empty, use /app
if [ "$AIGC_SERVICE_PREFIX" == "" ] ; then
    AIGC_SERVICE_PREFIX=/app
fi

# AIGC_SERVICE_EXEC is empty, use ‘python app.py’
if [ "$AIGC_SERVICE_EXEC" == "" ] ; then
    AIGC_SERVICE_EXEC="python -m uvicorn app:app --reload --host 0.0.0.0 --port 9000"
fi

# go to prefix dir
cd $AIGC_SERVICE_PREFIX
# excute
$AIGC_SERVICE_EXEC


