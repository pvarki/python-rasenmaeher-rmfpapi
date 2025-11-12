#!/bin/bash -l
. /container-init.sh

mkdir -p /ui_files/fake
if [ -d "/ui_build" ]; then
    echo "Copying UI files from /ui_build → /ui_files/fake ..."
    cp /ui_build/* /ui_files/fake/
else
    echo "No UI found at /ui_build, skipping copy."
fi

set -e
if [ "$#" -eq 0 ]; then
  # FIXME: can we know the traefik/nginx internal docker ip easily ?
  exec gunicorn "rmfpapi.app:get_app()" --bind 0.0.0.0:8001 --forwarded-allow-ips='*' -w 4 -k uvicorn.workers.UvicornWorker
else
  exec "$@"
fi
