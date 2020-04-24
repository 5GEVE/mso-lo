*** Settings ***
Resource   environment/variables.txt
Resource   NSLCMOperationKeywords.robot
Library    REST    ${MSO-LO_BASE_API}
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/
Suite Setup    Check resource existence

*** Test Cases ***
GET Information about an individual NS Instance
    [Documentation]    Test ID: 5.3.2.2.2
    ...    Test title: GET Information about an individual NS Instance
    ...    Test objective: The objective is to test that GET method returns an individual NS instance
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.3.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    GET IndividualNSInstance
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    NsInstance
