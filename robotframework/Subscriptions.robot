*** Settings ***
Resource    environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${NFVO_SCHEMA}://${NFVO_HOST}:${NFVO_PORT} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/

*** Test Cases ***
POST Create a new subscription
    [Documentation]    Test ID: 5.3.2.15.1
    ...    Test title: POST Create a new subscription
    ...    Test objective: The objective is to test that POST method create a subscription
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: subscription is created in the NFVO     
    POST subscriptions
    Check HTTP Response Status Code Is    201
    Check HTTP Response Header Contains    Location
    Check HTTP Response Body Json Schema Is    subscription
    

POST Create a new Subscription - DUPLICATION
    [Documentation]    Test ID: 5.3.2.15.2
    ...    Test title: POST Create a new subscription - DUPLICATION
    ...    Test objective: The objective is to test that POST method create a duplicate subscription 
    ...    Pre-conditions: a subscription shall already exist
    ...    Reference: clause 6.4.16.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: duplication supported by NFVO
    ...    Post-Conditions: duplicate subscription is created in the NFVO     
    POST subscriptions DUPLICATION
    Check HTTP Response Status Code Is    201
    Check HTTP Response Header Contains    Location
    Check HTTP Response Body Json Schema Is    subscription

POST Create a new Subscription - NO-DUPLICATION
    [Documentation]    Test ID: 5.3.2.15.3
    ...    Test title: POST Create a new subscription - NO-DUPLICATION
    ...    Test objective: The objective is to test that POST method cannot create a duplicate subscription 
    ...    Pre-conditions: a subscription shall already exist
    ...    Reference: clause 6.4.16.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: duplication NOT supported by NFVO
    ...    Post-Conditions: duplicate subscription is not created in the NFVO     
    POST subscriptions NO DUPLICATION
    Check HTTP Response Status Code Is    303
    Check HTTP Response Header Contains    Location

GET Subscriptions
    [Documentation]    Test ID: 5.3.2.15.4
    ...    Test title: GET Subscriptions
    ...    Test objective: The objective is to test that GET method  retrieve the list of existing subscriptions
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none    
    GET Subscriptions
    Check HTTP Response Status Code Is  200
    Check HTTP Response Body Json Schema Is  subscriptions

GET Subscription - Filter
    [Documentation]    Test ID: 5.3.2.15.5
    ...    Test title: GET Subscription - Filter
    ...    Test objective: The objective is Get the list of active subscriptions using a filter
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none    
    GET Subscriptions with filter
    Check HTTP Response Status Code Is  200
    Check HTTP Response Body Json Schema Is  subscriptions
    
GET subscriptions - Bad Request Invalid attribute-based filtering parameters
    [Documentation]    Test ID: 5.3.2.15.6
    ...    Test title: GET subscriptions - Bad Request Invalid attribute-based filtering parameters
    ...    Test objective: The objective is Get the list of active subscriptions using an invalid filter
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_VNFM
    ...    Applicability: none
    ...    Post-Conditions: none 
    Get subscriptions - invalid filter
    Check HTTP Response Status Code Is    400
    Check HTTP Response Body Json Schema Is    ProblemDetails

GET subscriptions with "all_fields" attribute selector
    [Documentation]    Test ID: 5.3.2.15.7
    ...    Test title: GET subscriptions with "all_fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active subscriptions with attribute selector
    ...    Pre-conditions: 
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:  
    ...    Post-Conditions: 
    Get subscriptions with all_fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions 

GET subscriptions with "exclude_default" attribute selector
    [Documentation]    Test ID: 5.3.2.15.8
    ...    Test title: GET subscriptions with "exclude_default" attribute selector
    ...    Test objective: The objective is to retrieve the list of active subscriptions with attribute selector
    ...    Pre-conditions: 
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:  
    ...    Post-Conditions: 
    Get subscriptions with exclude_default attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

GET subscriptions with "fields" attribute selector
    [Documentation]    Test ID: 5.3.2.15.9
    ...    Test title: GET subscriptions with "fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active subscriptions with attribute selector
    ...    Pre-conditions: 
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:  
    ...    Post-Conditions: 
    Get subscriptions with fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

GET subscriptions with "exclude_fields" attribute selector
    [Documentation]    Test ID: 5.3.2.15.10
    ...    Test title: GET subscriptions with "exclude_fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active subscriptions with attribute selector
    ...    Pre-conditions: 
    ...    Reference: clause 6.4.16.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:  
    ...    Post-Conditions: 
    Get subscriptions with exclude_fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions  
        
PUT subscriptions - Method not implemented
     [Documentation]    Test ID: 5.3.2.15.7
    ...    Test title: PUT subscriptions - Method not implemented
    ...    Test objective: The objective is to test that PUT method cannot modify a NS lifecycle management subscription
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    PUT subscriptions
    Check HTTP Response Status Code Is    405

PATCH subscriptions - Method not implemented
    [Documentation]    Test ID: 5.3.2.15.8
    ...    Test title: PATCH subscriptions - Method not implemented
    ...    Test objective: The objective is to test that PUT method cannot modify a NS lifecycle management subscription
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none
    PATCH subscriptions
    Check HTTP Response Status Code Is    405

DELETE subscriptions - Method not implemented
    [Documentation]    Test ID: 5.3.2.15.9
    ...    Test title: DELETE subscriptions - Method not implemented
    ...    Test objective: The objective is to test that DELETE method cannot modify a NS lifecycle management subscription
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.16.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: Subscription is not deleted
    DELETE subscriptions
    Check HTTP Response Status Code Is    405