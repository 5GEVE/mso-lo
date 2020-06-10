![Unit Tests](https://github.com/5GEVE/mso-lo/workflows/Unit%20Tests/badge.svg)

# 5G EVE - MSO-LO interface

MSO-LO is a REST API application to provide an
[ETSI SOL 005 v2.6.1](https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/001/02.06.01_60/gs_NFV-SOL001v020601p.pdf)
compliant interface towards various NFV orchestrators.

OpenAPI specification is provided on [Swagger Hub](https://app.swaggerhub.com/apis/zvfvrv/MSO-LO-new/) or in
[openapi directory](openapi).

The software is developed under the [5G EVE](https://www.5g-eve.eu/) project.

List of authors/contributors:

- Francesco Lombardo, CNIT
- Matteo Pergolesi, CNIT
- Grzesik Michal, Orange
- Panek Grzegorz, Orange
- Chabiera Michal, Orange

Software is distributed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

## Install guide

Copy the mock files (needed for a correct build):

```shell script
cd adaptation-layer/seed
cp nfvo_mock.json nfvo.json
cp nfvo_credentials_mock.json nfvo_credentials.json
```

### Environment with local database

Edit [docker-compose.yaml](docker-compose.yml) and disable site-inventory support.

```yaml
SITEINV: 'false'
```

Edit `adaptation-layer/seed/nfvo.json` and `adaptation-layer/seed/nfvo_credentials.json` (copied before)
and insert your NFVO data.

Deploy with:

```shell script
docker pull python:3.6-slim
docker-compose build
docker-compose up
```

### Environment with site-inventory (production)

If [site-inventory](https://github.com/5GEVE/site-inventory) is available in your environment,
edit [docker-compose.yaml](docker-compose.yml) and change the environment variables for the `flask` service:

```yaml
SITEINV: 'true'
SITEINV_HOST: '192.168.17.20'
SITEINV_PORT: '8087'
SITEINV_INTERVAL: '300'
```

Then, deploy with:

```shell script
docker pull python:3.6-slim
docker-compose build
docker-compose up
```

### Simple test

You can test the app with:

```shell script
curl --request GET --url http://127.0.0.1:80/nfvo
```
### Uninstall

To remove the containers and volumes, use:

```shell script
docker-compose down --remove-orphans --volumes
```

## Developer guide

### Branching model

There are two main branches:

- `master`: used for software releases, push not allowed
- `development`: used for daily work on code

To add a new feature, we follow this pattern:

1. Move to development branch: `git checkout development`
2. Create a new branch named after the feature you want to add. E.g.:
`git checkout -b onap_driver`
3. Work freely on the branch
4. When done, merge your branch into development:
`git checkout development; git merge --no-ff onap_driver;`

Note: The `--no-ff` option is useful to create a commit dedicated to the merge
and record the existence of the feature branch.
To add it to your git configuration so it is used by default (locally for this
repo), use:

```shell script
git config --add merge.ff false
```

### Environment setup

For dependencies we use [Pipenv](https://pipenv.readthedocs.io/en/latest/).
To setup the environment use:

**Remember to copy and edit the mock files as said in the [install guide](#install-guide)**

```shell script
git checkout development
cd adaptation_layer
pipenv install --dev
# Create database with mock data
pipenv run flask db upgrade
pipenv run python manage.py seed
# Run the flask app
FLASK_ENV=development flask run
```

Some features like notifications need [celery](https://docs.celeryproject.org/en/stable/index.html) and
[redis](https://redislabs.com/).
Simply setup a docker container with redis and run a celery worker.

```shell script
docker run -p 6379:6379 --name some-redis -d redis
export REDIS_HOST=localhost
celery -A tasks worker -B --loglevel=info
```

---

Please, always use `pipenv` to add/remove dependencies:

```shell script
pipenv install <package-name>

pipenv uninstall <package-name>
```

If everything works with the new dependencies, run `pipenv lock` and commit
both `Pipfile` and `Pipfile.lock`.

### Add a new NFVO driver

To create a new NFVO driver, it is enough to create a new python module
extending the `Driver` interface.
For example, let's create `adaptation_layer/driver/onap.py`:

```
from .interface import Driver

class ONAP(Driver):
    pass
```

Now you can start implementing the methods contained in the Driver interface.
Your IDE should suggest you to create stubs for methods to be overriden.

To enable a newly created driver, edit [manager.py](adaptation_layer/driver/manager.py).
The `get_driver()` method is simply a switch that returns an instance of the
proper driver.

### Add unit tests for a NFVO driver

In order to test our software against an NFVO NBI, we need to mock it.
For this purpose, we use [Prism](https://stoplight.io/open-source/prism/).
You can control the kind of HTTP response returned by Prism by modifying the request URL.
Example: `/nfvo/nfvo_osm1/ns?__code=200`

To add unit tests for a driver, create a new python file in `adaptation_layer/tests`.
Please refer to [test_osm.py](/adaptation_layer/tests/test_osm.py) for examples.

### Error handling

When throwing exceptions, please use the ones defined in [error_handler.py](adaptation_layer/error_handler.py).
This allows the application to correctly create the corresponding response and
status code.

## Tests

### Unit Tests

Unit tests can be executed by using Docker Compose files.
The following unit tests are currently available:

- [docker-compose.test-nfvo.yml](docker-compose.test-nfvo.yml) Test NFVO information retrieve
- [docker-compose.test-osm.yml](docker-compose.test-osm.yml) Test interactions with a mocked OSM
- [docker-compose.test-onap.yml](docker-compose.test-onap.yml) Test interactions with a mocked ONAP

Example:
```shell script
docker-compose --file docker-compose.test-osm.yml --project-name test-osm build
docker-compose --file docker-compose.test-osm.yml --project-name test-osm up --abort-on-container-exit --exit-code-from test-osm
```

*Note*: the `--project-name` parameter is necessary to distinguish test executions.

The file will run two containers:

1. A Prism server mocking the OSM NBI
2. A python container to execute unit tests

Unit tests execution for a new driver can be added by copying and modifying
[docker-compose.test-osm.yml](docker-compose.test-osm.yml).

### Integration tests

Integration tests are run with [Robot Framework](https://robotframework.org/).
Please refer to the specific [README](./adaptation_layer/robotframework/README.md).
