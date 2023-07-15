#!/bin/bash -l
if [ -f /data/persistent/firstrun.done ]
then
  echo "First run already cone"
else
  set -e
  /kw_product_init help
  date -u +"%Y%m%dT%H%M" >/data/persistent/firstrun.done
fi
