#!/bin/bash

# to be run in adaptation-layer module dir

export PIPENV_VENV_IN_PROJECT=1
export TESTING=True
pipenv  install --dev --skip-lock;
source .venv/bin/activate
nodeenv --python-virtualenv --jobs=8;
deactivate
source .venv/bin/activate
npm install --no-progress -g @stoplight/prism-cli;
prism mock tests/osm-openapi.yaml --port 9999 &>/dev/null &
PRISM_PID=$!
printf "$PRISM_PID\n"
sleep 2
cd tests &&
python test_osm.py
kill ${PRISM_PID}
exit 0

