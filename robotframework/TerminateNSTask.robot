*** Settings ***
Resource    environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${HTTP}://${MSO-LO_HOST}:${MSO-LO_PORT} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/

*** Test Cases ***
POST Terminate a NSInstance
    [Documentation]    Test ID: 5.3.2.7.1
    ...    Test title: POST Terminate a NSInstance
    ...    Test objective: The objective is to test that POST method terminate the NS
    ...    Pre-conditions: NS instance in INSTANTIATED state
    ...    Reference: clause 6.4.8.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: NS instance has NOT_INSTANTIATED state
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    202
    Check HTTP Response Header Contains    Location
    Check resource not_instantiated
    
POST Terminate a NSInstance Conflict
    [Documentation]    Test ID: 5.3.2.7.2
    ...    Test title: POST Terminate a NSInstance Conflict
    ...    Test objective: The objective is to test that POST method cannot terminate the NS because of conflict in resource status (i.e. the resource is not in INSTANTIATED state) 
    ...    Pre-conditions: NS instance is in NOT_INSTANTIATED state
    ...    Reference: clause 6.4.8.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: NS instance is in NOT_INSTANTIATED state
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    409
    Check HTTP Response Body Json Schema Is    ProblemDetails
    Check resource not_instantiated
    
GET Terminate NSInstance- Method not implemented
     [Documentation]    Test ID: 5.3.2.7.3
    ...    Test title: GET Terminate NSInstance- Method not implemented
    ...    Test objective: The objective is to test that GET method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.8.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    GET Terminate NSInstance
    Check HTTP Response Status Code Is    405
    
PUT Terminate NSInstance - Method not implemented
     [Documentation]    Test ID: 5.3.2.7.4
    ...    Test title: PUT Terminate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that PUT method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.8.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: resource state not modified
    PUT Terminate NSInstance
    Check HTTP Response Status Code Is    405
    
PATCH Terminate NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.7.5
    ...    Test title: PATCH Terminate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that PATCH method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.8.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: resource state not modified
    PATCH Terminate NSInstance
    Check HTTP Response Status Code Is    405

DELETE Terminate NSInstance - Method not implemented
         [Documentation]    Test ID: 5.3.2.7.5
    ...    Test title: DELETE Terminate NSInstance - Method not implemented
    ...    Test objective: The objective is to test that DELETE method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.8.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: resource state not modified
    DELETE Terminate NSInstance
    Check HTTP Response Status Code Is    405
    
    