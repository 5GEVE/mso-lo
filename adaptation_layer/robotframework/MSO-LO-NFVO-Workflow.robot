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

GET NFVO List
    [Documentation]    Test ID: mso-lo-test-
    ...    Test title: GET NFVO List
    ...    Test objective: The objective is to test the workflow for retriving the NFVO list
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET NFVO List
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${nfvo_list_schema}

GET Individual NFVO informations
    [Documentation]    Test ID: mso-lo-test-
    ...    Test title: GET Individual NFVO informations
    ...    Test objective: The objective is to test the workflow for retriving the NFVO informations
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET IndividualNFVO
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    ${nfvo_schema}

GET Individual NFVO informations inexistent
    [Documentation]    Test ID: mso-lo-test-
    ...    Test title: GET Individual NFVO informations inexistent
    ...    Test objective: The objective is to test the workflow for retriving the NFVO informations
    ...    Pre-conditions: none
    ...    Post-Conditions: none
    GET IndividualNFVO inexistent
    Check HTTP Response Status Code Is    404
