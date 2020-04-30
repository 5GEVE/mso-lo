*** Settings ***
Resource    environment/variables.txt
Variables   ../adaptation_layer/tests/response_schemas.py
Resource   NSLCMOperationKeywords.robot
Resource   NFVOOperationKeywords.robot
Library    REST    ${MSO-LO_BASE_API}
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/


*** Test Cases ***

NS Instance List
    [Documentation]    Test ID: mso-lo-test-3.1
    ...    Test title: NS Instance List
    ...    Test objective: The objective is to test the workflow for retriving the NS instance list
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET NsInstances
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${ns_list_schema}

NS Instance Creation
    [Documentation]    Test ID: mso-lo-test-3.2
    ...    Test title: NS Instance Creation
    ...    Test objective: The objective is to test the workflow for Creating a NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: The NS lifecycle management operation occurrence is in NOT_ISTANTIATED state
    POST New nsInstance
    Check HTTP Response Status Code Is    201
    Check HTTP Response Header Contains    Location
    # Check HTTP Response Body Json Schema Is    NsIdentifierCreationNotification
    Check NS Id
    Check resource not_instantiated

NS Instance Creation Bad Request
    [Documentation]    Test ID: mso-lo-test-3.2.1
    ...    Test title: NS Instance Creation Bad Request
    ...    Test objective: The objective is to test the workflow for Creating a NS instance with a bad request
    ...    Pre-conditions: none
    ...    Post-Conditions: Status code 400
    POST New nsInstance with invalid request body
    Check HTTP Response Status Code Is    400

GET Information about an individual NS Instance
    [Documentation]    Test ID: mso-lo-test-3.3
    ...    Test title: GET Information about an individual NS Instance
    ...    Test objective: The objective is to test that GET method returns an individual NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET IndividualNSInstance
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${ns_schema}

GET Information about an inexistent individual NS Instance
    [Documentation]    Test ID: mso-lo-test-3.3.1
    ...    Test title: GET Information about an inexistent individual NS Instance
    ...    Test objective: The objective is to test that GET method returns an inexistent individual NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: Status code 404
    GET IndividualNSInstance inexistent
    Check HTTP Response Status Code Is    404

NS Instance Instantiate
    [Documentation]    Test ID: mso-lo-test-3.4
    ...    Test title: NS Instance Instantiate
    ...    Test objective: The objective is to test the workflow for Instantiate a NS instance
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 202
    Check resource existence
    Check resource not_instantiated
    POST Instantiate nsInstance
    Check HTTP Response Status Code Is    202
    Check HTTP Response Header Contains    Location
    Check Operation Occurrence Id

NS LCM OP Occurrence Instantiate
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: NS LCM OP Occurrence Instantiate
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 202
    GET Individual NS LCM OP Occurrence
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_schema}

NS Instance Terminate
    [Documentation]    Test ID: mso-lo-test-3.
    ...    Test title: Terminate NS Instance
    ...    Test objective: The objective is to test the workflow for Terminate a NS instance
    ...    Pre-conditions: the resource is in INSTANTIATED state
    ...    Post-Conditions:  the resource is in NOT_INSTANTIATED state
    Check resource existence
    Check resource instantiated
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    202
    Check Operation Occurrence Id

NS LCM OP Occurrence Terminate
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: NS LCM OP Occurrence Terminate
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    GET Individual NS LCM OP Occurrence
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_schema}

NS LCM OP Occurrences
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: NS LCM OP Occurrences
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrences
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    GET NS LCM OP Occurrences
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_list_schema}

NS Instance Deletion
    [Documentation]    Test ID: mso-lo-test-3.6
    ...    Test title: NS Instance Deletion
    ...    Test objective: The objective is to test the workflow for Deleting a NS instance
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 204
    Check resource not_instantiated
    DELETE IndividualNSInstance
    Check HTTP Response Status Code Is    204
