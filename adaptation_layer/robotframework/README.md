## Tests with Robot Framework

The `.robot` scripts in this folder perform integration tests of the `mso-lo` application
against a real instance of a NFVO.

To execute the tests you need:

- An instance of `mso-lo` up and running
- An instance of a real NFVO
- Correct communication between the two above (check your database)

Check the file [variables.robot](./environment/variables.robot) and change the variables according
to your setup. The important variables to change are:

- `${MSO-LO_HOST}`
- `${MSO-LO_PORT}`
- `${nfvoId}`
- `${nsdId}` (this is the NSD to be instantiated during the tests, pick something simple)

Example of execution:

```shell script
$ cd {project-dir}/adaptation_layer
# activate the virtual env
$ pipenv shell
$ cd ./robotframework
# export mso-lo openapi file path relative to this directory
$ export OPENAPI_PATH=../../openapi/MSO-LO-swagger-resolved.yaml
$ robot --outputdir output MSO-LO-LCM-Workflow.robot MSO-LO-NFVO-Workflow.robot
```

Script [MSO-LO-LCM-Workflow.robot](./MSO-LO-LCM-Workflow.robot) contains a workflow that
instantiates and terminates a Network Service on the configured NFVO.
Some test cases include features to wait for the NS to be deployed. Maximum waiting time is set to
2 minutes. You can increase it if it is not enough by changing `${MAXIMUM_WAIT}` variable in
[variables.robot](./environment/variables.robot).
