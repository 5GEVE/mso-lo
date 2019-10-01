#!/bin/bash

pipenv install --dev &&
source .venv/bin/activate &&
nodeenv -p &&
deactivate &&
source .venv/bin/activate &&
npm install -g @stoplight/prism-cli &&
prism mock tests/osm_fixed.yaml &

# run pytest

