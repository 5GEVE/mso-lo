*** Settings ***
Resource   environment/variables.txt
Library    REST     ${MSO-LO_BASE_API}
Library    JSONLibrary
Library    Process
Library    JSONSchemaLibrary    schemas/
Library    OperatingSystem


*** Keywords ***

Check Operation Occurrence Id
    Set Global Variable    ${nsLcmOpOccId}    ${response[0]['headers']['Location']}
    Should Not Be Empty    ${nsLcmOpOccId}

Check subscription existence
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    Integer    response status    200

Check Fail not supported
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    # how to check if Fail is not supported? Also In Sol002

Check Cancel not supported
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    # how to check if Cancel is not supported? Also In Sol002

Check Continue not supported
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    # how to check if Continue is not supported? Also In Sol002

Check retry not supported
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    # how to check if retry is not supported? Also In Sol002

Check Rollback not supported
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    # how to check if rollback is not supported? Also In Sol002

Check resource FAILED_TEMP
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    String    response body operationState    FAILED_TEMP

Check resource not
    [Arguments]   ${status}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    Should Not Be Equal As Strings  response body operationState    ${status}

Check Operation Notification Status is
    [Arguments]    ${status}
    Check Operation Notification    NsLcmOperationOccurrenceNotification   ${status}

Check Operation Notification
    [Arguments]    ${element}    ${status}=""
    ${json}=	Get File	schemas/${element}.schema.json
    Configure Notification Forward    ${element}    ${callback_endpoint}    ${callback_endpoint_fwd}
    Configure Notification Status Handler    ${callback_endpoint_fwd}    ${status}
    Wait Until Keyword Succeeds    2 min   10 sec   Verify Mock Expectation    ${notification_request}
    Clear Requests    ${callback_endpoint}
    Clear Requests    ${callback_endpoint_fwd}

Configure Notification Forward
    [Arguments]    ${element}    ${endpoint}    ${endpoint_fwd}
    ${BODY}=	evaluate	json.loads('''${json}''')	json
    Log  Creating mock HTTP forward to handle ${element}
    &{notification_tmp}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON_SCHEMA"    body=${BODY}
    &{notification_fwd}=  Create Mock Http Forward	${endpoint_fwd}
    Create Mock Expectation With Http Forward  ${notification_tmp}  ${notification_fwd}

Configure Notification Status Handler
    [Arguments]    ${endpoint}    ${status}=""
    Run Keyword If   ${status}!=""  set to dictionary    ${json["notificationStatus"]}    dp=${status}
    ${BODY}=    evaluate    json.dumps(${json})    json
    Log  Creating mock request and response to handle ${element}
    &{notification_request}=  Create Mock Request Matcher	POST  ${endpoint}  body_type="JSON"    body=${BODY}
    &{notification_response}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${notification_request}  ${notification_response}

Check resource operationState is
    [Arguments]    ${state}
    String    ${response[0]['body']['operationState']}   ${state}

Check resource instantiated
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    String    response body nsState    INSTANTIATED

Check resource not_instantiated
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    String    response body nsState    NOT_INSTANTIATED

Check operation resource state is FAILED_TEMP
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    String    response body nsState    FAILED_TEMP
Check operation resource state is not FAILED_TEMP
    Check operation resource state is FAILED_TEMP
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    String  response body nsState  not  FAILED_TEMP

Check resource is finally failed
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    String    response body nsState    FINALLY_FAILED

Launch another LCM operation
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/scaleNsToLevelRequest.json
    Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale_to_level    ${body}
    Integer    response status    202

Check resource existence
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    Integer    response status    200

Check HTTP Response Status Code Is
    [Arguments]    ${expected_status}
    Log    Validate Status code
    Should Be Equal as Strings  ${response[0]['status']}    ${expected_status}
    Log    Status code validated

Check HTTP Response Header Contains
    [Arguments]    ${HEADER_TOCHECK}
    Should Contain     ${response[0]['headers']}    ${HEADER_TOCHECK}
    Log    Header is present

Check HTTP Response Body Json Schema Is
    [Arguments]    ${input}
    ${schema} =  Catenate  ${input}.schema.json
    Validate Json    ${schema}    ${response[0]['body']}
    Log    Json Schema Validation OK

Check HTTP Response Header ContentType is
    [Arguments]    ${expected_contentType}
    Log    Validate content type
    Should Be Equal as Strings   ${response[0]['headers']['Content-Type']}    ${expected_contentType}
    Log    Content Type validated

POST New nsInstance
    Log    Create NS instance by POST to ${apiRoot}/${nfvoId}/ns_instances
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/CreateNsRequest.json
    Post    ${apiRoot}/${nfvoId}/ns_instances  ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST New nsInstance with invalid request body
    Log    Create NS instance by POST to ${apiRoot}/${nfvoId}/ns_instances with bad request body
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Post    ${apiRoot}/${nfvoId}/ns_instances
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET NsInstances
    Log    Query NS The GET method queries information about multiple NS instances.
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}


GET NsInstance Invalid Attribute-Based filtering parameter
    Log    Query NS The GET method queries information about multiple NS instances.
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get   ${apiRoot}/${nfvoId}/ns_instances?attribute_not_exist=some_value
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET NsInstance Invalid Attribute Selector
    Log    Query NS The GET method queries information about multiple NS instances.
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances?fields=wrong_field
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

Get NSInstances with all_fields attribute selector
    Log    Get the list of NSInstances, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_instances?exclude_default
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

Get NSInstances with exclude_default attribute selector
    Log    Get the list of NSInstances, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_instances?exclude_default
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

Get NSInstances with fields attribute selector
    Log    Get the list of NSInstances, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_instances?fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

Get NSInstances with exclude_fields attribute selector
    Log    Get the list of NSInstances, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_instances?exclude_fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

PUT NSInstances
    log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH NSInstances
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE NSInstances
    log    Trying to perform a DELETE. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST IndividualNSInstance
    Log    Trying to perform a POST. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET IndividualNSInstance
    Log    Trying to get information about an individual NS instance
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET IndividualNSInstance inexistent
    Log    Trying to get information about an individual NS instance
    Set Headers    {"Accept":"${ACCEPT}"}
    Set Headers    {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceIdinexistent}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}


PUT IndividualNSInstance
    Log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH IndividualNSInstance
    Log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE IndividualNSInstance
    log    Trying to delete an individual VNF instance
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}


DELETE IndividualNSInstance Conflict
    log    Trying to delete an individual VNF instance
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${ConflictNsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}


DELETE Instantiate NSInstance
    log    Trying to delete an instantiate NS instance. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Instantiate NSInstance
    log    Trying to patch an instantiate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Instantiate NSInstance
    log    Trying to put an instantiate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Instantiate NSInstance
    log    Trying to get an instantiate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Instantiate nsInstance
    Log    Trying to Instantiate a ns Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/InstantiateNsRequest.json
    Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate    ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Scale NSInstance
    log    Trying to delete an Scale NS instance. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Scale NSInstance
    log    Trying to patch an Scale NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Scale NSInstance
    log    Trying to put an Scale NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Scale NSInstance
    log    Trying to get an Scale NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST scale nsInstance
	Log    Trying to Instantiate a scale NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/ScaleNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale    ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Update NSInstance
    log    Trying to delete an Update NS instance. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/update
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Update NSInstance
    log    Trying to patch an Update NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/update
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Update NSInstance
    log    Trying to put an Update NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/update
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Update NSInstance
    log    Trying to get an Update NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/update
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Update NSInstance
	Log    Trying to Instantiate a Update NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/UpdateNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/update    ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Heal NSInstance
    log    Trying to Delete an Heal NS instance. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Heal NSInstance
    log    Trying to patch an Heal NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Heal NSInstance
    log    Trying to put an Heal NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Heal NSInstance
    log    Trying to get an Heal NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Heal NSInstance
	Log    Trying to Instantiate a Heal NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/HealNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal    ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Terminate NSInstance
    log    Trying to Delete an Terminate NS instance. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/terminate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Terminate NSInstance
    log    Trying to patch an Terminate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/terminate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Terminate NSInstance
    log    Trying to put an Terminate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/terminate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Terminate NSInstance
    log    Trying to Get an Terminate NS instance. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/terminate
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Terminate NSInstance
	Log    Trying to Instantiate a Terminate NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/TerminateNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/terminate    ${body}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST NS LCM OP Occurrences
    log    Trying to perform a POST. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT NS LCM OP Occurrences
    log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH NS LCM OP Occurrences
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE NS LCM OP Occurrences
    log    Trying to perform a DELETE. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET NS LCM OP Occurrences
    Log    Query status information about multiple NS lifecycle management operation occurrences.
	Set Headers  {"Accept":"${ACCEPT}"}
	Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
	Log    Execute Query and validate response
	Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET NS LCM OP Occurrences Invalid attribute-based filtering parameters
    Log    Query status information about multiple NS lifecycle management operation occurrences.
	Set Headers  {"Accept":"${ACCEPT}"}
	Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
	GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?${NEG_FILTER}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET NS LCM OP Occurrences Invalid attribute selector
    Log    Query status information about multiple NS lifecycle management operation occurrences.
    Set Headers  {"Accept":"${ACCEPT}"}
	Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
	GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?${NEG_SELECTOR}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}
Get NS LCM OP Occurrences with all_fields attribute selector
    Log    Query status information about multiple NS lifecycle management operation occurrences, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?exclude_default
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get NS LCM OP Occurrences with exclude_default attribute selector
    Log    Query status information about multiple NS lifecycle management operation occurrences using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?exclude_default
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get NS LCM OP Occurrences with fields attribute selector
    Log    Query status information about multiple NS lifecycle management operation occurrences, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get NS LCM OP Occurrences with exclude_fields attribute selector
    Log    Query status information about multiple NS lifecycle management operation occurrences, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/ns_lcm_op_occs?exclude_fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

POST Individual NS LCM OP Occurrence
    log    Trying to perform a POST. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Individual NS LCM OP Occurrence
    log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Individual NS LCM OP Occurrence
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Individual NS LCM OP Occurrence
    log    Trying to perform a DELETE. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Individual NS LCM OP Occurrence
    Log    Query status information about individual NS lifecycle management operation occurrence.
	Set Headers  {"Accept":"${ACCEPT}"}
	Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
	Log    Execute Query and validate response
	Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Retry operation task
    log    Trying to perform a GET. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Retry operation task
    log    Trying to perform a PUT. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Retry operation task
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Retry operation task
    log    Trying to perform a DELETE. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Retry operation task
    Log    Retry a NS lifecycle operation if that operation has experienced a temporary failure
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Rollback operation task
    log    Trying to perform a GET. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Rollback operation task
    log    Trying to perform a PUT. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Rollback operation task
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Rollback operation task
    log    Trying to perform a DELETE. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Rollback operation task
    Log    Rollback a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Continue operation task
    log    Trying to perform a GET. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Continue operation task
    log    Trying to perform a PUT. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Continue operation task
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Continue operation task
    log    Trying to perform a DELETE. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Continue operation task
    Log    Continue a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Fail operation task
    log    Trying to perform a GET. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Fail operation task
    log    Trying to perform a PUT. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Fail operation task
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Fail operation task
    log    Trying to perform a DELETE. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Fail operation task
    Log    Fail a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Cancel operation task
    log    Trying to perform a GET. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Cancel operation task
    log    Trying to perform a PUT. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Cancel operation task
    Log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Patch    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Cancel operation task
    Log    Trying to perform a DELETE. This method should not be implemented
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Cancel operation task
    Log    Cancel a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT subscriptions
    Log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/subscriptions
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH subscriptions
    Log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/subscriptions
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE subscriptions
    Log    Trying to perform a DELETE. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/subscriptions
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST subscriptions
    Log    Create subscription instance by POST to ${apiRoot}/${nfvoId}/subscriptions
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/LccnSubscriptionRequest.json
    Post    ${apiRoot}/${nfvoId}/subscriptions    ${body}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST subscriptions DUPLICATION
    Log    Trying to create a subscription with an already created content
    Pass Execution If    ${NFVO_DUPLICATION} == 0    NFVO is not permitting duplication. Skipping the test
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/LccnSubscriptionRequest.json
    Post    ${apiRoot}/${nfvoId}/subscriptions    ${body}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST subscriptions NO DUPLICATION
    Log    Trying to create a subscription with an already created content
    Pass Execution If    ${NFVO_DUPLICATION} == 1    NFVO is permitting duplication.
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/LccnSubscriptionRequest.json
    Post    ${apiRoot}/${nfvoId}/subscriptions    ${body}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}


GET Subscriptions
    Log    Get the list of active subscriptions
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Get    ${apiRoot}/${nfvoId}/subscriptions
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

Get subscriptions with all_fields attribute selector
    Log    Get the list of active subscriptions, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?all_fields
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get subscriptions with exclude_default attribute selector
    Log    Get the list of active subscriptions, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?exclude_default
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get subscriptions with fields attribute selector
    Log    Get the list of active subscriptions, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}
Get subscriptions with exclude_fields attribute selector
    Log    Get the list of active subscriptions, using fields
    Set Headers    {"Accept": "${ACCEPT_JSON}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?exclude_fields=${fields}
    ${output}=    Output    response
    Set Suite Variable    ${response}    ${output}

GET subscriptions with filter
    Log    Get the list of active subscriptions using a filter
    Set Headers    {"Accept": "${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?${sub_filter}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

Get subscriptions - invalid filter
    Log    Get the list of active subscriptions using an invalid filter
    Set Headers    {"Accept": "${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization": "${AUTHORIZATION}"}
    GET    ${apiRoot}/${nfvoId}/subscriptions?${sub_filter_invalid}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Individual Subscription
    log    Trying to perform a POST. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Post    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PUT Individual Subscription
    log    Trying to perform a PUT. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Put    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

PATCH Individual Subscription
    log    Trying to perform a PATCH. This method should not be implemented
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Patch    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Individual subscription
    log    Trying to get information about an individual subscription
    Set Headers    {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Individual subscription
    log    Try to delete an individual subscription
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Operation occurrence
    log    The POST method delivers a notification from the server to the client.
    ${json}=	Get File	schemas/NsLcmOperationOccurrenceNotification.schema.json
    ${BODY}=	evaluate	json.loads('''${json}''')	json
    Log  Creating mock request and response to handle NSLcmOperationOccurrenceNotification
    &{req}=  Create Mock Request Matcher	POST  ${callback_endpoint}  body_type="JSON_SCHEMA"    body=${BODY}
    &{rsp}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${req}  ${rsp}
    Sleep  ${sleep_interval}
    Log  Verifying results
    Verify Mock Expectation  ${req}
    Log  Cleaning the endpoint
    Clear Requests  ${callback_endpoint}

POST Id creation
    log    The POST method delivers a notification from the server to the client.
    ${json}=	Get File	schemas/NsIdentifierCreationNotification.schema.json
    ${BODY}=	evaluate	json.loads('''${json}''')	json
    Log  Creating mock request and response to handle NsIdentifierCreationNotification
    &{req}=  Create Mock Request Matcher	POST  ${callback_endpoint}}  body_type="JSON_SCHEMA"    body=${BODY}
    &{rsp}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${req}  ${rsp}
    Sleep  ${sleep_interval}
    Log  Verifying results
    Verify Mock Expectation  ${req}
    Log  Cleaning the endpoint
    Clear Requests  ${callback_endpoint}

POST Id deletion
    log    The POST method delivers a notification from the server to the client.
    ${json}=	Get File	schemas/NsIdentifierDeletionNotification.schema.json
    ${BODY}=	evaluate	json.loads('''${json}''')	json
    Log  Creating mock request and response to handle NsIdentifierDeletionNotification
    &{req}=  Create Mock Request Matcher	POST  ${callback_endpoint}  body_type="JSON_SCHEMA"    body=${BODY}
    &{rsp}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${req}  ${rsp}
    Sleep  ${sleep_interval}
    Log  Verifying results
    Verify Mock Expectation  ${req}
    Log  Cleaning the endpoint
    Clear Requests  ${callback_endpoint}

GET Notification endpoint
    log    The GET method allows the server to test the notification endpoint
    &{req}=  Create Mock Request Matcher	GET  ${callback_endpoint}
    &{rsp}=  Create Mock Response	headers="Content-Type: application/json"  status_code=204
    Create Mock Expectation  ${req}  ${rsp}
    Sleep  ${sleep_interval}
    Verify Mock Expectation  ${req}
    Clear Requests  ${callback_endpoint}

PUT notification
    Log  PUT Method not implemented
    &{req}=  Create Mock Request Matcher	PUT  ${callback_endpoint}
    &{rsp}=  Create Mock Response  status_code=405
    Create Mock Expectation  ${req}  ${rsp}
    Sleep  ${sleep_interval}
    Log  Verifying results
    Verify Mock Expectation  ${req}
    Log  Cleaning the endpoint
    Clear Requests  ${callback_endpoint}
