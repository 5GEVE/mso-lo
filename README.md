# 5G EVE - MSO-LO interface

[OpenAPI spec](https://app.swaggerhub.com/apis/zvfvrv/MSO-LO-new/3.1)

## Install guide

We use Docker Compose for deployment. From the repository main directory, run:

```
docker-compose build
docker-compose run
```

The app is now litening on `http://0.0.0.0:5000`.
You can test it with:

```
curl --request GET --url http://127.0.0.1:80/nfvo
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

```
git config --add merge.ff false
```

### Environment setup

For dependencies we use [Pipenv](https://pipenv.readthedocs.io/en/latest/).
To setup the environment use:

```
git checkout development
cd adaptation_layer
pipenv install --dev
# Run the flask app
pipenv run python app.py
```

Please, always use `pipenv` to add dependencies:

```
pipenv install <package-name>
```

After that, please commit `Pipfile` and `Pipfile.lock`.

### Add a new NFVO driver

To create a new NFVO driver, it is enough to create a new python module
extending the `Driver` interface.
For example, let's create `/adaptation_layer/driver/onap.py`:

```
from .interface import Driver

class ONAP(Driver):
```

Now you can start implementing the methods contained in the Driver interface.
Your IDE should suggest you to create stubs for methods to be overriden.

### Error handling

When throwing exceptions, please use the ones defined in `error_handler.py`.
This allows the application to correctly create the corresponding response and
status code.

### Update the driver manager

To enable a newly created driver, edit `/adaptation_layer/driver/manager.py`.
The `get_driver()` method is simply a switch that returns an instance of the
proper driver.

### Tests

In order to test our software against an NFVO NBI, we need to mock it.
For this purpose, we use [Prism](https://stoplight.io/open-source/prism/).
You can control the kind of HTTP response returned by Prism by modifying the
request URL.
Example: `/nfvo/nfvo_osm1/ns?__code=200`
Please refer to `/adaptation_layer/tests/test_osm.py` for examples.

To add unit tests for a driver, create a new python file in
`/adaptation_layer/tests`.
For example: `/adaptation_layer/tests/test_onap.py`

Unit tests can be run by using Docker Compose files. Example:

```
docker-compose -f docker-compose.test-osm.yml -p test-osm up
```

The file will run two containers:

1. A Prism server mocking the OSM NBI
2. A python container to execute unit tests

Unit tests execution for a new driver can be added by copying and modifyng
`docker-compose.test-osm.yml`.

