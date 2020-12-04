# Tests with Robot Framework

The `.robot` scripts in this folder perform integration tests of the `mso-lo` application
against a real instance of a NFVO or RANO.

To execute the tests you need:

- An instance of `mso-lo` up and running
- An instance of a real NFVO or RANO
- An instante of the [IWF Repository](https://github.com/5GEVE/iwf-repository)
- Correct communication between the components above

## Configuration

Check the file [variables.robot](./environment/variables.robot).
Variables that can be customized are provided at the beginning of the file.

> Note: use at least 4 spaces between variable name and value, or use tabs

Setup the protocol, host and port where mso-lo application is listening.

```
${MSO-LO_HOST}      localhost
${MSO-LO_PORT}      80
${HTTP}    http
```

Choose what type of orchestrator you want to test, `nfvo` or `rano`, and provide its ID.
The ID comes from the IWF Repository.

```
${apiRoot}        nfvo
${nfvoId}         1
```

In the IWF Repository, set the credentials for your orchestrator.
Assuming the values above, and that the IWF Repository is hosted at `localhost:8087`:

```
curl --request PATCH \
  --url http://localhost:8087/nfvOrchestrators/1 \
  --header 'Content-Type: application/json' \
  --data '{
	"credentials": {
		"host": "192.168.100.2",
		"port": 9999,
		"username": "admin",
		"password": "admin",
		"project": "admin"
	}
}'
```

Select the UUID of the NSD you want to deploy for the test.
It must be available in your NFVO or RANO catalog.

```
${nsdId}    5821d426-4c51-4be0-a849-5218a09f0d72
```

### Optional

The following settings can be used to associate a Virtual Link of your NSD to a network existing on your VIM.
Please provide both names or **remove/comment the two lines**.

> Note: If you want to use this you also need to register your network in the
> IWF repository.

```
${vimNetworkName}   test
${vldName}          mgmt_vl
```

The following setting is used to deploy the VNFs of your service on multiple VIMs available in your NFVO/RANO.
Please provide the UUIDs as shown below or **remove/comment the line**.

```
${vimAccountIds}    ['64690905-0fe0-4dc4-967c-292eb497e46f', '444bd22e-dd1a-4672-b12b-2604f21f50e6']
```

Script [MSO-LO-LCM-Workflow.robot](./MSO-LO-LCM-Workflow.robot) contains a workflow that
instantiates and terminates a Network Service on the configured NFVO.
Some test cases include features to wait for the NS to be deployed.
Maximum waiting time is set to 2 minutes.
You can increase it if it is not enough:

```
${MAX_WAIT}   2 min
```

MSO-LO can send notifications about the operation status to an endpoint.
You can set it with:

```
${notificationUri}   http://192.168.18.14:8083/
```

## Execution:

```shell script
$ cd {project-dir}/adaptation_layer
# activate the virtual env
$ pipenv shell
$ cd ./robotframework
# export mso-lo openapi file path relative to this directory
$ export OPENAPI_PATH=../../openapi/MSO-LO-swagger-resolved.yaml
$ robot --outputdir output MSO-LO-LCM-Workflow.robot MSO-LO-NFVO-Workflow.robot
```
