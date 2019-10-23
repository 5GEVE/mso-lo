#!/bin/bash

# to be run in adaptation-layer module dir

export PIPENV_VENV_IN_PROJECT=1
export TESTING=True
pipenv install --dev &&
pipenv run nodeenv --debug --prebuilt --python-virtualenv --jobs=8 &&
pipenv run npm install -g @stoplight/prism-cli &&
pipenv run prism mock tests/osm-openapi.yaml --port 9999 &>/dev/null;
PRISM_PID=$!
printf "$PRISM_PID"
sleep 1
printf "run python here"
#pipenv run cd tests && python test_osm.py
kill ${PRISM_PID}
exit 0
