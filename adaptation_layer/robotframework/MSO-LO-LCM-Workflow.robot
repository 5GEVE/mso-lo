*** Settings ***
Resource    environment/variables.robot
Variables   ${SCHEMAS_PATH}
Resource   NSLCMOperationKeywords.robot
Resource   NFVOOperationKeywords.robot
Library    REST    ${MSO-LO_BASE_API}
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/


*** Test Cases ***
POST NS Instance Creation
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.2
    ...    Test title: POST NS Instance Creation
    ...    Test objective: The objective is to test the workflow for Creating a NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: The NS lifecycle management operation occurrence is in NOT_ISTANTIATED state
    POST New nsInstance
    Check HTTP Response Status Code Is    201
    Check HTTP Response Header Contains    Location
    Check HTTP Response Body Json Schema Is   ${ns_schema}
    Check NS Id
    Run Keyword If    "${apiRoot}" == "nfvo"
    ...    Check VNF Ids
    ...    ELSE IF    "${apiRoot}" == "rano"
    ...    Log    No vnfInstance with rano
    ...    ELSE
    ...    Fatal Error    Unknown value for variable apiRoot
    Check resource not_instantiated
    POST New Subscription Good
    Check Sub Id

GET NS Instance List
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.1
    ...    Test title: GET NS Instance List
    ...    Test objective: The objective is to test the workflow for retriving the NS instance list
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET NsInstances
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${ns_list_schema}

GET Information about an individual NS Instance
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.3
    ...    Test title: GET Information about an individual NS Instance
    ...    Test objective: The objective is to test that GET method returns an individual NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET IndividualNSInstance
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${ns_schema}

POST NS Instance Instantiate
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.4
    ...    Test title: POST NS Instance Instantiate
    ...    Test objective: The objective is to test the workflow for Instantiate a NS instance
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 202
    Check resource existence
    Check resource not_instantiated
    Run Keyword If    "${apiRoot}" == "nfvo"
    ...    POST Instantiate nsInstance with vnf/vld in additionalParamsForNs
    ...    ELSE IF    "${apiRoot}" == "rano"
    ...    POST Instantiate nsInstance with SapData
    ...    ELSE
    ...    Fatal Error    Unknown value for variable apiRoot
    Check HTTP Response Status Code Is    202
    Check HTTP Response Header Contains    Location
    Check Operation Occurrence Id

GET NS LCM OP Occurrence Instantiate PROCESSING
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: GET NS LCM OP Occurrence Instantiate PROCESSING
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    GET Individual NS LCM OP Occurrence
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_schema}
    Check resource lcmOperationType is  INSTANTIATE
    Check resource operationState is    PROCESSING

GET NS LCM OP Occurrence Instantiate COMPLETED
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.6
    ...    Test title: GET NS LCM OP Occurrence Instantiate COMPLETED
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    Wait Until Keyword Succeeds    ${MAX_WAIT}    ${INTERVAL_WAIT}    Run Keywords
    ...   GET Individual NS LCM OP Occurrence
    ...   AND   Check resource operationState is    COMPLETED

GET NS LCM OP Occurrences
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: GET LCM OP Occurrences
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrences
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    GET NS LCM OP Occurrences
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_list_schema}

POST NS Instance Terminate
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.
    ...    Test title: POST Terminate NS Instance
    ...    Test objective: The objective is to test the workflow for Terminate a NS instance
    ...    Pre-conditions: the resource is in INSTANTIATED state
    ...    Post-Conditions:  the resource is in NOT_INSTANTIATED state
    Check resource existence
    Check resource instantiated
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    202
    Check Operation Occurrence Id

GET NS LCM OP Occurrence Terminate PROCESSING
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: GET NS LCM OP Occurrence Terminate PROCESSING
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    GET Individual NS LCM OP Occurrence
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is  ${ns_lcm_op_occ_schema}
    Check resource lcmOperationType is  TERMINATE
    Check resource operationState is    PROCESSING

GET NS LCM OP Occurrence Terminate COMPLETED
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: GET NS LCM OP Occurrence Terminate COMPLETED
    ...    Test objective: The objective is to test the workflow for retrive NS LCM OP Occurrence
    ...    Pre-conditions: none
    ...    Post-Conditions: status code 200
    Wait Until Keyword Succeeds    ${MAX_WAIT}    ${INTERVAL_WAIT}    Run Keywords
    ...   GET Individual NS LCM OP Occurrence
    ...   AND   Check resource operationState is    COMPLETED

POST NS Instance Delete
    [Tags]    instantiate-terminate-workflow
    [Documentation]    Test ID: mso-lo-test-3.6
    ...    Test title: POST NS Instance Delete
    ...    Test objective: The objective is to test the workflow for Deleting a NS instance
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 204
    Sleep  5s
    Check resource not_instantiated
    DELETE IndividualNSInstance
    Check HTTP Response Status Code Is    204
    DELETE Individual Subscription Good

POST NS Instance Creation Bad Request
    [Tags]    standalone
    [Documentation]    Test ID: mso-lo-test-3.2.1
    ...    Test title: POST Instance Creation Bad Request
    ...    Test objective: The objective is to test the workflow for Creating a NS instance with a bad request
    ...    Pre-conditions: none
    ...    Post-Conditions: Status code 400
    POST New nsInstance with invalid request body
    Check HTTP Response Status Code Is    400

GET Information about an inexistent individual NS Instance
    [Tags]    standalone
    [Documentation]    Test ID: mso-lo-test-3.3.1
    ...    Test title: GET Information about an inexistent individual NS Instance
    ...    Test objective: The objective is to test that GET method returns an inexistent individual NS instance
    ...    Pre-conditions: none
    ...    Post-Conditions: Status code 404
    GET IndividualNSInstance inexistent
    Check HTTP Response Status Code Is    404
