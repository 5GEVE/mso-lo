*** Settings ***
Resource    environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${MSO-LO_BASE_API} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/

*** Test Cases ***
POST NS LCM occurrences - Method not implemented
    [Documentation]    Test ID: 5.3.2.8.1
    ...    Test title: POST NS LCM occurrences - Method not implemented
    ...    Test objective: The objective is to test that POST method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.9.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	POST NS LCM OP Occurrences
	Check HTTP Response Status Code Is    405

GET status information about multiple NS LCM occurrences   
     [Documentation]    Test ID: 5.3.2.8.2
    ...    Test title: GET status information about multiple NS LCM occurrences
    ...    Test objective: The objective is to test that GET method returns a list of LCM occurrences of the NS
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	GET NS LCM OP Occurrences
	Check HTTP Response Status Code Is    200
	Check HTTP Response Body Json Schema Is    NsLcmOpOccs

GET status information about multiple NS LCM occurrences Bad Request Invalid attribute-based filtering parameters
    [Documentation]    Test ID: 5.3.2.8.3
    ...    Test title: GET status information about multiple NS LCM occurrences Bad Request Invalid attribute-based filtering parameters
    ...    Test objective: The objective is to test that GET method fail because of wrong query parameter
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO, Invalid filter parameter
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	GET NS LCM OP Occurrences Invalid attribute-based filtering parameters
	Check HTTP Response Status Code Is    400
	Check HTTP Response Body Json Schema Is    ProblemDetails

GET status information about multiple NS LCM occurrences Bad Request Invalid attribute selector
    [Documentation]    Test ID: 5.3.2.8.4
    ...    Test title: GET status information about multiple NS LCM occurrences Bad Request Invalid attribute selector
    ...    Test objective: The objective is to test that GET method fail because of wrong attributes selector
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO, Invalid attribute selector
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	GET NS LCM OP Occurrences Invalid attribute selector
	Check HTTP Response Status Code Is    400
	Check HTTP Response Body Json Schema Is    ProblemDetails

GET status information about multiple NS LCM occurrences with "all_fields"   
     [Documentation]    Test ID: 5.3.2.8.5
    ...    Test title: GET status information about multiple NS LCM occurrences with "all_fields"
    ...    Test objective: The objective is to test that GET method returns a list of LCM occurrences of the NS
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	Get NS LCM OP Occurrences with all_fields attribute selector
	Check HTTP Response Status Code Is    200
	Check HTTP Response Body Json Schema Is    NsLcmOpOccs

GET status information about multiple NS LCM occurrences with "exclude_default"   
     [Documentation]    Test ID: 5.3.2.8.6
    ...    Test title: GET status information about multiple NS LCM occurrences with "exclude_default"
    ...    Test objective: The objective is to test that GET method returns a list of LCM occurrences of the NS
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	Get NS LCM OP Occurrences with exclude_default attribute selector
	Check HTTP Response Status Code Is    200
	Check HTTP Response Body Json Schema Is    NsLcmOpOccs

GET status information about multiple NS LCM occurrences with "fields"   
     [Documentation]    Test ID: 5.3.2.8.7
    ...    Test title: GET status information about multiple NS LCM occurrences with "fields"
    ...    Test objective: The objective is to test that GET method returns a list of LCM occurrences of the NS
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	Get NS LCM OP Occurrences with fields attribute selector
	Check HTTP Response Status Code Is    200
	Check HTTP Response Body Json Schema Is    NsLcmOpOccs

GET status information about multiple NS LCM occurrences with "exclude_fields"   
     [Documentation]    Test ID: 5.3.2.8.8
    ...    Test title: GET status information about multiple NS LCM occurrences with "exclude_fields"
    ...    Test objective: The objective is to test that GET method returns a list of LCM occurrences of the NS
    ...    Pre-conditions: At least one LCM occurrences available in the NFVO
    ...    Reference: clause 6.4.9.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
	Get NS LCM OP Occurrences with exclude_fields attribute selector
	Check HTTP Response Status Code Is    200
	Check HTTP Response Body Json Schema Is    NsLcmOpOccs

PUT status information about multiple NS LCM occurrences - Method not implemented
    [Documentation]    Test ID: 5.3.2.8.5
    ...    Test title: PUT status information about multiple NS LCM occurrences - Method not implemented
    ...    Test objective: The objective is to test that PUT method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.9.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    PUT NS LCM OP Occurrences
    Check HTTP Response Status Code Is    405

PATCH status information about multiple NS LCM occurrences - Method not implemented
    [Documentation]    Test ID: 5.3.2.8.6
    ...    Test title: PATCH status information about multiple NS LCM occurrences - Method not implemented
    ...    Test objective: The objective is to test that PATCH method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.9.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    PATCH NS LCM OP Occurrences
    Check HTTP Response Status Code Is    405

DELETE status information about multiple NS LCM occurrences - Method not implemented
    [Documentation]    Test ID: 5.3.2.8.7
    ...    Test title: DELETE status information about multiple NS LCM occurrences - Method not implemented
    ...    Test objective: The objective is to test that DELETE method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.9.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    DELETE NS LCM OP Occurrences
    Check HTTP Response Status Code Is    405
    
