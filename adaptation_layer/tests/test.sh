#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1
export TESTING=True
pipenv install --dev &&
source .venv/bin/activate &&
nodeenv -p &
deactivate &&
source .venv/bin/activate &&
npm install -g @stoplight/prism-cli &&
prism mock tests/osm-openapi.yaml --port 9999 &

# run pytest

