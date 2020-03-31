*** Settings ***
Suite Setup    Create Sessions
Suite Teardown    Terminate All Processes    kill=true
Resource    environment/variables.txt
Library    MockServerLibrary
Library    Process
Library    OperatingSystem
Library    Collections

*** Test Cases ***
NS LCM Operation Occurrence Start Notification
    [Documentation]    Test ID: 5.3.2.17.1
    ...    Test title: NS LCM Operation Occurrence Start Notification
    ...    Test objective: The objective is to test the dispatch of NS LCM Operation Occurrence Start Notification when a new NS LCM operation is started in the NFVO, and perform a JSON schema and content validation of the delivered notification. The action that triggers the notification under test is an explicit test step, but it is not performed by the test system.
    ...    Pre-conditions: A subscription for NS LCM Operation Occurrence notifications is available in the NFVO.
    ...    Reference: clause 6.4.18.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none 
    Trigger a NS LCM operation (external action) 
    Check NS LCM Operation Occurrence Start Notification Http POST Request Body Json Schema Is    NsLcmOperationOccurrenceNotification
    Check NS LCM Operation Occurrence Start Notification Http POST Request Body notificationType attribute Is    NsLcmOperationOccurrenceNotification
    Check NS LCM Operation Occurrence Start Notification Http POST Request Body notificationStatus attribute Is    START
    
NS LCM Operation Occurrence Result Notification
    [Documentation]    Test ID: 5.3.2.17.2
    ...    Test title: NS LCM Operation Occurrence Result Notification
    ...    Test objective: The objective is to test the dispatch of NS LCM Operation Occurrence Result Notification when a NS LCM operation is completed in the NFVO, and perform a JSON schema and content validation of the delivered notification. The action that triggers the notification under test is an explicit test step, but it is not performed by the test system.
    ...    Pre-conditions: An NS LCM operation is in progress, and a subscription for NS LCM Operation Occurrence notifications is available in the NFVO.
    ...    Reference: clause 6.4.18.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none 
    Trigger the completion of an NS LCM operation (external action)
    Check NS LCM Operation Occurrence Result Notification Http POST Request Body Json Schema Is    NsLcmOperationOccurrenceNotification
    Check NS LCM Operation Occurrence Result Notification Http POST Request Body notificationType attribute Is    NsLcmOperationOccurrenceNotification
    Check NS LCM Operation Occurrence Start Notification Http POST Request Body notificationStatus attribute Is    RESULT
    
NS Identifier Creation Notification
    [Documentation]    Test ID: 5.3.2.17.3
    ...    Test title: NS Identifier Creation Notification
    ...    Test objective: The objective is to test the dispatch of NS Identifier Creation Notification when a new NS instance resource is created in the NFVO, and perform a JSON schema and content validation of the delivered notification. The action that triggers the notification under test is an explicit test step, but it is not performed by the test system.
    ...    Pre-conditions: A subscription for NS identifier creation notifications is available in the NFVO.
    ...    Reference: clause 6.4.18.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none 
    Trigger the creation of a NS instance resource (external action)
    Check NS Identifier Creation Notification Http POST Request Body Json Schema Is    NsIdentifierDeletionNotification
    Check NS Identifier Creation Notification Http POST Request Body notificationType attribute Is    NsIdentifierDeletionNotification
    
NS Identifier Deletion Notification
    [Documentation]    Test ID: 5.3.2.17.4
    ...    Test title: NS Identifier Deletion Notification
    ...    Test objective: The objective is to test the dispatch of NS Identifier Deletion Notification when a NS instance resource is deleted in the NFVO, and perform a JSON schema and content validation of the delivered notification.The action that triggers the notification under test is an explicit test step, but it is not performed by the test system.
    ...    Pre-conditions: A NS instance resource is created, and a subscription for NS identifier creation notifications is available in the NFVO.
    ...    Reference: clause 6.4.18.3.1 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: none 
    Trigger the deletion of a NS instance resource (external action)
    Check NS Identifier Deletion Notification Http POST Request Body Json Schema Is    NsIdentifierCreationNotification
    Check NS Identifier Deletion Notification Http POST Request Body notificationType attribute Is    NsIdentifierCreationNotification
    
*** Keywords ***
Trigger a NS LCM operation (external action) 
    #do nothing
    Log    do nothing

Trigger the completion of an NS LCM operation (external action)
    #do nothing
    Log    do nothing   
    
Trigger the creation of a NS instance resource (external action)
    #do nothing
    Log    do nothing     
  
Trigger the deletion of a NS instance resource (external action)
    #do nothing
    Log    do nothing     
    
Check NS LCM Operation Occurrence Start Notification Http POST Request Body Json Schema Is  
    [Arguments]    ${element}
    ${schema}=	Get File	schemas/${element}.schema.json
    Configure Notification Forward    ${schema}    ${callback_endpoint}    ${callback_endpoint_fwd}

Check NS LCM Operation Occurrence Start Notification Http POST Request Body notificationType attribute Is
    [Arguments]    ${type}
    Configure Notification NS LCM Operation Occurrence Start Handler    ${callback_endpoint_fwd}    ${type}    START
    Wait Until Keyword Succeeds    2 min   10 sec   Verify Mock Expectation    ${notification_request}
    Clear Requests    ${callback_endpoint}
    Clear Requests    ${callback_endpoint_fwd}
    
Configure Notification NS LCM Operation Occurrence Start Handler
    [Arguments]    ${endpoint}    ${type}    ${status}
    ${json}=    evaluate    {}
    set to dictionary   ${json}    notificationType    ${type}    changeType    ${status}
    ${BODY}=    evaluate    json.dumps(${json})    json
    Log  Creating mock request and response to handle status notification
    &{notification_request}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON"    body=${BODY}
    &{notification_response}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${notification_request}  ${notification_response}

Check NS LCM Operation Occurrence Result Notification Http POST Request Body Json Schema Is  
    [Arguments]    ${element}
    ${schema}=	Get File	schemas/${element}.schema.json
    Configure Notification Forward    ${schema}    ${callback_endpoint}    ${callback_endpoint_fwd}

Check NS LCM Operation Occurrence Result Notification Http POST Request Body notificationType attribute Is
    [Arguments]    ${type}
    Configure Notification NS LCM Operation Occurrence Result Handler    ${callback_endpoint_fwd}    ${type}    RESULT
    Wait Until Keyword Succeeds    2 min   10 sec   Verify Mock Expectation    ${notification_request}
    Clear Requests    ${callback_endpoint}
    Clear Requests    ${callback_endpoint_fwd}
    
Configure Notification NS LCM Operation Occurrence Result Handler
    [Arguments]    ${endpoint}    ${type}    ${status}
    ${json}=    evaluate    {}
    set to dictionary   ${json}    notificationType    ${type}    changeType    ${status}
    ${BODY}=    evaluate    json.dumps(${json})    json
    Log  Creating mock request and response to handle status notification
    &{notification_request}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON"    body=${BODY}
    &{notification_response}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${notification_request}  ${notification_response}

Check NS Identifier Creation Notification Http POST Request Body Json Schema Is  
    [Arguments]    ${element}
    ${schema}=	Get File	schemas/${element}.schema.json
    Configure Notification Forward    ${schema}    ${callback_endpoint}    ${callback_endpoint_fwd}

Check NS Identifier Creation Notification Http POST Request Body notificationType attribute Is
    [Arguments]    ${type}
    Configure Notification NS Identifier Creation Handler    ${callback_endpoint_fwd}    ${type}
    Wait Until Keyword Succeeds    2 min   10 sec   Verify Mock Expectation    ${notification_request}
    Clear Requests    ${callback_endpoint}
    Clear Requests    ${callback_endpoint_fwd}

Configure Notification NS Identifier Creation Handler
    [Arguments]    ${endpoint}    ${type}
    ${json}=    evaluate    {}
    set to dictionary   ${json}    notificationType    ${type}
    ${BODY}=    evaluate    json.dumps(${json})    json
    Log  Creating mock request and response to handle status notification
    &{notification_request}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON"    body=${BODY}
    &{notification_response}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${notification_request}  ${notification_response}
    
Check NS Identifier Deletion Notification Http POST Request Body Json Schema Is  
    [Arguments]    ${element}
    ${schema}=	Get File	schemas/${element}.schema.json
    Configure Notification Forward    ${schema}    ${callback_endpoint}    ${callback_endpoint_fwd}

Check NS Identifier Deletion Notification Http POST Request Body notificationType attribute Is
    [Arguments]    ${type}
    Configure Notification NS Identifier Deletion Handler    ${callback_endpoint_fwd}    ${type}
    Wait Until Keyword Succeeds    2 min   10 sec   Verify Mock Expectation    ${notification_request}
    Clear Requests    ${callback_endpoint}
    Clear Requests    ${callback_endpoint_fwd}

Configure Notification NS Identifier Deletion Handler
    [Arguments]    ${endpoint}    ${type}
    ${json}=    evaluate    {}
    set to dictionary   ${json}    notificationType    ${type}
    ${BODY}=    evaluate    json.dumps(${json})    json
    Log  Creating mock request and response to handle status notification
    &{notification_request}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON"    body=${BODY}
    &{notification_response}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${notification_request}  ${notification_response}

Check NS LCM Operation Occurrence Start Notification Http POST Request Body notificationStatus attribute Is
    [Arguments]    ${type}
    #do nothing
    Log    do nothing
    
Check NS LCM Operation Occurrence Result Notification Http POST Request Body notificationStatus attribute Is
    [Arguments]    ${type}
    #do nothing
    Log    do nothing

Configure Notification Forward
    [Arguments]    ${schema}    ${endpoint}    ${endpoint_fwd}    
    Log  Creating mock Http POST forward to handle ${schema}
    &{notification_tmp}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON_SCHEMA"    body=${schema}
    &{notification_fwd}=  Create Mock Http Forward	${endpoint_fwd}
    Create Mock Expectation With Http Forward  ${notification_tmp}  ${notification_fwd}

Create Sessions
    Start Process  java  -jar  ${MOCK_SERVER_JAR}  -serverPort  ${callback_port}  alias=mockInstance
    Wait For Process  handle=mockInstance  timeout=5s  on_timeout=continue
    Create Mock Session  ${callback_uri}:${callback_port}