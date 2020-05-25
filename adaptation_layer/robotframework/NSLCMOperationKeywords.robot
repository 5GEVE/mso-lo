*** Settings ***
Resource   environment/variables.txt
Library    REST     ${MSO-LO_BASE_API}
Library    JSONLibrary
Library    Process
Library    jsonschema
Library    OperatingSystem

*** Keywords ***

Check NS Id
    Set Global Variable    ${nsInstanceId}    ${response[0]['body']['id']}
    Should Not Be Empty    ${nsInstanceId}

Check VNF Ids
    ${vnfInstances}=    set variable    ${response[0]['body']['vnfInstance']}
    ${vnfInstances}=    evaluate   [v['id'] for v in ${vnfInstances}]
    Set Global Variable    ${vnfInstanceIds}    ${vnfInstances}
    Log    ${vnfInstances}
    Should Not Be Empty    ${vnfInstanceIds}

Check Operation Occurrence Id
    ${nsLcmOpOcc}=    set variable    ${response[0]['headers']['Location']}
    # using a basic regex, it can be improved
    ${nsLcmOpOcc}=    evaluate    re.search(r'(/nfvo/.*/ns_lcm_op_occs/(.*))', '''${nsLcmOpOcc}''').group(2)    re
    Set Global Variable    ${nsLcmOpOccId}    ${nsLcmOpOcc}
    Should Not Be Empty    ${nsLcmOpOccId}
    Log    ${nsLcmOpOccId}

Check resource FAILED_TEMP
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}
    String    response body operationState    FAILED_TEMP

Check resource operationState is not
    [Arguments]   ${state}
    Should Be Not Equal As Strings    ${response[0]['body']['operationState']}    ${state}
    Log     State is ${state}

Check resource operationState is
    [Arguments]   ${state}
    Should Be Equal As Strings    ${response[0]['body']['operationState']}    ${state}
    Log     State is ${state}

Check resource lcmOperationType is
    [Arguments]   ${type}
    Should Be Equal As Strings    ${response[0]['body']['lcmOperationType']}    ${type}
    Log     Type is ${type}

Check Operation Notification Status is
    [Arguments]    ${status}
    Check Operation Notification    NsLcmOperationOccurrenceNotification   ${status}

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
    [Arguments]    ${input_schema}
    validate    instance=${response[0]['body']}    schema=${input_schema}
    Log    ${response[0]['body']}
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
    ${body}=    Load JSON From File    jsons/CreateNsRequest.json
    ${body}=    Update Value To Json    ${body}    $.nsdId    ${nsdId}
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

DELETE IndividualNSInstance
    log    Trying to delete an individual NS instance
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Instantiate nsInstance with vnf in additionalParamsForNs
    Log    Trying to Instantiate a ns Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Load JSON From File    jsons/InstantiateNsRequest.json
    ${vnf}=    set variable    []
    ${vnf}=    evaluate    [{"vnfInstanceId": vnfId,"vimAccountId": random.choice(${vimAccountIds})} for vnfId in ${vnfInstanceIds}]    random
    Log    ${vnf}
    ${body}=    Update Value To Json    ${body}    $.additionalParamsForNs.vnf    ${vnf}
    Log    ${body}
    Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/instantiate    ${body}
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

POST scale nsInstance
	Log    Trying to Instantiate a scale NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/ScaleNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/scale    ${body}
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

POST Heal NSInstance
	Log    Trying to Instantiate a Heal NS Instance
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/HealNsRequest.json
	Post    ${apiRoot}/${nfvoId}/ns_instances/${nsInstanceId}/heal    ${body}
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

GET NS LCM OP Occurrences
    Log    Query status information about multiple NS lifecycle management operation occurrences.
	Set Headers  {"Accept":"${ACCEPT}"}
	Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
	Log    Execute Query and validate response
	Get    ${apiRoot}/${nfvoId}/ns_lcm_op_occs
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

POST Retry operation task
    Log    Retry a NS lifecycle operation if that operation has experienced a temporary failure
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/retry
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Rollback operation task
    Log    Rollback a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/rollback
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Continue operation task
    Log    Continue a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/continue
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Fail operation task
    Log    Fail a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/fail
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST Cancel operation task
    Log    Cancel a NS lifecycle operation task
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Log    Execute Query and validate response
    Post    ${apiRoot}/${nfvoId}/ns_lcm_op_occs/${nsLcmOpOccId}/cancel
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

POST New Subscription Good
    Log    Create subscription instance by POST to ${apiRoot}/${nfvoId}/subscriptions
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    Get File    jsons/LccnSubscriptionRequest.json
    Post    ${apiRoot}/${nfvoId}/subscriptions    ${body}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

POST New Subscription Bad
    Log    Create subscription instance by POST to ${apiRoot}/${nfvoId}/subscriptions
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    ${body}=    {"bad": "request"}
    Post    ${apiRoot}/${nfvoId}/subscriptions    ${body}
	${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Individual Subscription Good
    log    Trying to get information about an individual subscription
    Set Headers    {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET Individual Subscription Not Found
    log    Trying to get information about an individual subscription
    Set Headers    {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}/subscriptions/-1
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Individual Subscription Good
    log    Try to delete an individual subscription
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

DELETE Individual Subscription Not Found
    log    Try to delete an individual subscription
    Set Headers  {"Accept":"${ACCEPT}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Delete    ${apiRoot}/${nfvoId}/subscriptions/${subscriptionId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

