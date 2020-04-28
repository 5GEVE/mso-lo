*** Settings ***
Resource    environment/variables.txt
Resource   NSLCMOperationKeywords.robot
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
    # Check HTTP Response Body Json Schema Is    NsInstances


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
    #Check HTTP Response Body Json Schema Is    NsInstance

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
    #Check Operation Notification Status is    START
    #Check Operation Notification Status is    RESULT
    #Check resource instantiated

NS Instance Terminate
    [Documentation]    Test ID: mso-lo-test-3.5
    ...    Test title: Terminate NS Instance
    ...    Test objective: The objective is to test the workflow for Terminate a NS instance
    ...    Pre-conditions: the resource is in INSTANTIATED state
    ...    Post-Conditions:  the resource is in NOT_INSTANTIATED state
    Check resource existence
    Check resource instantiated
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    202
    Check Operation Occurrence Id
    # Check Operation Notification Status is    START
    # Check Operation Notification Status is    RESULT
    Check resource not_instantiated

NS Instance Deletion
    [Documentation]    Test ID: mso-lo-test-3.6
    ...    Test title: NS Instance Deletion
    ...    Test objective: The objective is to test the workflow for Deleting a NS instance
    ...    Pre-conditions: the resource is in NOT_INSTANTIATED state
    ...    Post-Conditions: status code 204
    Check resource not_instantiated
    DELETE IndividualNSInstance
    Check HTTP Response Status Code Is    204
    #Check HTTP Response Body Json Schema Is    NsIdentifierDeletionNotification
