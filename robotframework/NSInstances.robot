*** Settings ***
Resource    environment/variables.txt
Resource   NSLCMOperationKeywords.robot
Library    REST    ${MSO-LO_BASE_API}
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/

*** Test Cases ***
POST Create a new NsInstance
    [Documentation]    Test ID: 5.3.2.1.1
    ...    Test title: POST Create a new NsInstance
    ...    Test objective: The objective is to test the creation of a new Ns Instances and perform a JSON schema validation of the collected instance data structure
    ...    Pre-conditions: None.
    ...    Reference: clause 6.4.2.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none.
    ...    Post-Conditions: A Ns instance is instantiated.
    POST New nsInstance
    Check HTTP Response Status Code Is    201
    Check HTTP Response Header Contains    Location
    Check HTTP Response Body Json Schema Is    NsInstance

GET information about multiple NS instances
    [Documentation]    Test ID: 5.3.2.1.2
    ...    Test title: GET information about multiple NS instances
    ...    Test objective: The objective is to test the retrieval of all the available NS Instances and perform a JSON schema and content validation of the collected instance data structure
    ...    Pre-conditions: An existing Ns instance.
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none.
    ...    Post-Conditions: none.
    GET NsInstances
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is    NsInstances

GET information about multiple NS instances Bad Request Invalid attribute-based filtering parameters
    [Documentation]    Test ID: 5.3.2.1.3
    ...    Test title: GET information about multiple NS instances Bad Request Invalid attribute-based filtering parameters
    ...    Test objective: The objective is to test the retrieval of all the available NS Instances using attribute-based filter and perform a JSON schema and content validation of the collected instance data structure
    ...    Pre-conditions: A Ns instance is instantiated, a bad filter parameter (filter parameters are listed in Table 6.4.2.3.2-1  - ETSI GS NFV-SOL 005 [3] v2.4.1).
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none.
    ...    Post-Conditions: none.
    GET NsInstance Invalid Attribute-Based filtering parameter
    Check HTTP Response Status Code Is    400
    Check HTTP Response Body Json Schema Is    ProblemDetails

GET information about multiple NS instances Bad Request Invalid attribute selector
    [Documentation]    Test ID: 5.3.2.1.4
    ...    Test title: GET information about multiple NS instances Bad Request Invalid attribute selector
    ...    Test objective: The objective is to test the retrieval of all the available NS Instances using attribute-based filter and perform a JSON schema and content validation of the collected instance data structure
    ...    Pre-conditions: A Ns instance is instantiated,  a bad attribute selector (attribute selectors are listed in Table 6.4.2.3.2-1  - ETSI GS NFV-SOL 005 [3] v2.4.1).
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none.
    ...    Post-Conditions: none.
    
    Check HTTP Response Status Code Is    400
    Check HTTP Response Body Json Schema Is    ProblemDetails
GET NSInstances with "all_fields" attribute selector
    [Documentation]    Test ID: 5.3.2.1.5
    ...    Test title: GET NSInstances with "all_fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active NSInstances with attribute selector
    ...    Pre-conditions:
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:
    ...    Post-Conditions:
    Get NSInstances with all_fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

GET NSInstances with "exclude_default" attribute selector
    [Documentation]    Test ID: 5.3.2.1.6
    ...    Test title: GET NSInstances with "exclude_default" attribute selector
    ...    Test objective: The objective is to retrieve the list of active NSInstances with attribute selector
    ...    Pre-conditions:
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:
    ...    Post-Conditions:
    Get NSInstances with exclude_default attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

GET NSInstances with "fields" attribute selector
    [Documentation]    Test ID: 5.3.2.1.7
    ...    Test title: GET NSInstances with "fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active NSInstances with attribute selector
    ...    Pre-conditions:
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:
    ...    Post-Conditions:
    Get NSInstances with fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

GET NSInstances with "exclude_fields" attribute selector
    [Documentation]    Test ID: 5.3.2.1.8
    ...    Test title: GET NSInstances with "exclude_fields" attribute selector
    ...    Test objective: The objective is to retrieve the list of active NSInstances with attribute selector
    ...    Pre-conditions:
    ...    Reference: clause 6.4.2.3.2 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability:
    ...    Post-Conditions:
    Get NSInstances with exclude_fields attribute selector
    Check HTTP Response Status Code Is    200
    Check HTTP Response Body Json Schema Is   FmSubscriptions

PUT NSInstances - Method not implemented
    [Documentation]    Test ID: 5.3.2.1.9
    ...    Test title: PUT Individual NS instance - Method not implemented
    ...    Test objective: The objective is to test that PUT method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.2.3.3 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not modified by the operation
    PUT NSInstances
    Check HTTP Response Status Code Is    405

PATCH NSInstances - Method not implemented
     [Documentation]    Test ID: 5.3.2.1.10
    ...    Test title: PATCH NSInstances - Method not implemented
    ...    Test objective: The objective is to test that PATCH method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.2.3.4 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not modified by the operation
    PATCH NSInstances
    Check HTTP Response Status Code Is    405

DELETE NSInstances - Method not implemented
     [Documentation]    Test ID: 5.3.2.1.11
    ...    Test title: DELETE NSInstances - Method not implemented
    ...    Test objective: The objective is to test that DELETE method is not implemented
    ...    Pre-conditions: none
    ...    Reference: clause 6.4.2.3.5 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: The NS instance is not deleted by the operation
    DELETE NSInstances
    Check HTTP Response Status Code Is    405
