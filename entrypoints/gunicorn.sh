#!/usr/bin/env bash
set -e

export APP_MODULE=${APP_MODULE:-"${MODULE_NAME:-src.main}:${VARIABLE_NAME:-app}"}
export GUNICORN_CONF=${GUNICORN_CONF:-/src/gunicorn/gunicorn_conf.py}
export WORKER_CLASS=${WORKER_CLASS:-uvicorn.workers.UvicornWorker}

gunicorn --forwarded-allow-ips "*" -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"