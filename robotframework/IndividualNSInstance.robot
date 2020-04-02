*** Settings ***
Resource   environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${MSO-LO_BASE_API} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/
Suite Setup    Check resource existence

*** Test Cases ***
POST Individual NSInstance - Method not implemented
    [Documentation]    Test ID: 5.3.2.2.1
    ...    Test title: POST Individual NSInstance - Method not implemented
    ...    Test objective: The objective is to test that POST method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.3.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not created on the NFVO
    POST IndividualNSInstance
    Check HTTP Response Status Code Is    405

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
    
PUT Individual NSInstance - Method not implemented 
    [Documentation]    Test ID: 5.3.2.2.3
    ...    Test title: PUT Individual NSInstance - Method not implemented
    ...    Test objective: TThe objective is to test that PUT method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.3.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not modified on the NFVO
    PUT IndividualNSInstance
    Check HTTP Response Status Code Is    405

PATCH Individual NSInstance - Method not implemented 
    [Documentation]    Test ID: 5.3.2.2.4
    ...    Test title: PATCH Individual NSInstance - Method not implemented
    ...    Test objective: The objective is to test that PATCH method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.3.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not modified on the NFVO
    PATCH IndividualNSInstance
    Check HTTP Response Status Code Is    405

DELETE Individual NSInstance
     [Documentation]    Test ID: 5.3.2.2.5
    ...    Test title: DELETE Individual NSInstance
    ...    Test objective: The objective is to test that DELETE method delete a not INSTANTIATED NS instance
    ...    Pre-conditions: NS instance is not INSTANTIATED .
    ...    Reference: clause 6.4.3.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is deleted from the NFVO
    DELETE IndividualNSInstance    
    Check HTTP Response Status Code Is    204

DELETE Individual NSInstance Conflict
    [Documentation]    Test ID: 5.3.2.2.6
    ...    Test title: DELETE Individual NSInstance Conflict
    ...    Test objective: The objective is to test that DELETE method cannot delete an INSTANTIATED NS instance
    ...    Pre-conditions: one instance of a NS in INSTANTIATED state
    ...    Reference: clause 6.4.3.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not deleted from the NFVO
    DELETE IndividualNSInstance
    Check HTTP Response Status Code Is    409
    Check HTTP Response Body Json Schema Is    ProblemDetails
