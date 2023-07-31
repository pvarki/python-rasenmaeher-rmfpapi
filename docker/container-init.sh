#!/bin/bash -l
if [ -f /data/persistent/firstrun.done ]
then
  echo "First run already cone"
else
  set -e
  # Resolve our magic names to docker internal ip
  sed 's/.*localmaeher.*//g' /etc/hosts >/etc/hosts.new && cat /etc/hosts.new >/etc/hosts
  echo "$(getent hosts host.docker.internal | awk '{ print $1 }') localmaeher.pvarki.fi mtls.localmaeher.pvarki.fi" >>/etc/hosts
  # Do the normal init
  /kw_product_init init /pvarki/kraftwerk-init.json
  # FIXME: This should be done natively in the FastAPI app
  /kw_product_init ready --productname "fakeproduct" --apiurl "https://api.example.com:8443/"  --userurl "https://example.com/"  /pvarki/kraftwerk-init.json
  date -u +"%Y%m%dT%H%M" >/data/persistent/firstrun.done
fi
