#!/bin/bash -l
if [ -f /data/persistent/firstrun.done ]
then
  echo "First run already cone"
else
  set -e
  /kw_product_init init /pvarki/kraftwerk-init.json
  # the ready endpoint does not exist yet so this will always fail
  # /kw_product_init ready /pvarki/kraftwerk-init.json
  date -u +"%Y%m%dT%H%M" >/data/persistent/firstrun.done
fi
