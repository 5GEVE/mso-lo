*** Settings ***
Resource    environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${HTTP}://${MSO-LO_HOST}:${MSO-LO_PORT} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/
Suite Setup    Check resource existence

*** Test Cases ***
POST Instantiate a nsInstance
    [Documentation]    Test ID: 5.3.2.3.1
    ...    Test title: POST Instantiate a nsInstance
    ...    Test objective: The objective is to test that POST method instantiate a new NS instance
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.4.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is instantiated on the NFVO
    POST Instantiate nsInstance
    Check HTTP Response Status Code Is    202
    Check HTTP Response Header Contains    Location
    Check resource INSTANTIATED

POST Instantiate a nsInstance Conflict
    [Documentation]    Test ID: 5.3.2.3.2
    ...    Test title: POST Instantiate a nsInstance Conflict
    ...    Test objective: The objective is to test that the operation cannot be performed due to a conflict with the state of resource (i.e. the resource is in INSTANTIATED state)
    ...    Pre-conditions: resource is in INSTANTIATED state
    ...    Reference: clause 6.4.4.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not instantiated on the NFVO
    POST Instantiate nsInstance
    Check HTTP Response Status Code Is    409
    Check HTTP Response Body Json Schema Is    ProblemDetails
    Check resource not_instantiated
    
GET Instantiate NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.3.3
    ...    Test title: GET Instantiate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that the operation cannot be performed due because method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.4.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none.
    GET Instantiate NSInstance
    Check HTTP Response Status Code Is    405
    
PUT Instantiate NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.3.4
    ...    Test title: PUT Instantiate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that the operation cannot be performed due because method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.4.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none.
    PUT Instantiate NSInstance
    Check HTTP Response Status Code Is    405
    
PATCH Instantiate NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.3.5
    ...    Test title: PATCH Instantiate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that the operation cannot be performed due because method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.4.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none.
    PATCH Instantiate NSInstance
    Check HTTP Response Status Code Is    405

DELETE Instantiate NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.3.6
    ...    Test title: DELETE Instantiate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that the operation cannot be performed due because method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.4.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none.
    DELETE Instantiate NSInstance
    Check HTTP Response Status Code Is    405