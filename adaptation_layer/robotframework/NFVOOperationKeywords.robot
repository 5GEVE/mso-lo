*** Settings ***
Resource   environment/variables.robot
Library    REST     ${MSO-LO_BASE_API}
Library    JSONLibrary
Library    Process
Library    JSONSchemaLibrary    schemas/
Library    OperatingSystem


*** Keywords ***

GET NFVO List
    Log    Retrive NFVO list
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET IndividualNFVO
    Log    Retrive NFVO
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoId}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}

GET IndividualNFVO inexistent
    Log    Retrive NFVO
    Set Headers  {"Accept":"${ACCEPT}"}
    Set Headers  {"Content-Type": "${CONTENT_TYPE}"}
    Run Keyword If    ${AUTH_USAGE} == 1    Set Headers    {"Authorization":"${AUTHORIZATION}"}
    Get    ${apiRoot}/${nfvoIdinexistent}
    ${outputResponse}=    Output    response
	Set Global Variable    @{response}    ${outputResponse}
