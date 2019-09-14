To mock OSM NBI you can use [Prism](https://stoplight.io/open-source/prism/).

Command: `~/.npm/bin/prism mock ./osm_fixed.yaml`

Request example: `curl http://127.0.0.1:4010/nsd/v1/ns_descriptors -H "Authorization: Bearer 0faketoken0"`

