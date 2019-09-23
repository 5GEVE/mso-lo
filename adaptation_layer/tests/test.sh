#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1
pipenv install --dev &&
source .venv/bin/activate &&
nodeenv -p &&
deactivate &&
source .venv/bin/activate &&
npm install -g @stoplight/prism-cli &&
prism mock tests/osm_fixed.yaml &

# run pytest

