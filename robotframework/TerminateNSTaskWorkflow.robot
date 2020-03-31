*** Settings ***
Resource    environment/variables.txt 
Resource   NSLCMOperationKeywords.robot   
Library    REST    ${NFVO_SCHEMA}://${NFVO_HOST}:${NFVO_PORT} 
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/
Suite Setup       Initialize System
Suite Teardown    Terminate All Processes    kill=true

*** Test Cases ***
Terminate Flow of NS lifecycle management operations
    [Documentation]    Test ID: 5.3.2.22
    ...    Test title: Terminate Flow of NS lifecycle management operations
    ...    Test objective: The objective is to test the workflow for Terminate a NS instance
    ...    Pre-conditions: the resource is in INSTANTIATED state
    ...    Reference: clause 6.4.8 - ETSI GS NFV-SOL 005 [3] v2.4.1
    ...    Config ID: Config_prod_NFVO
    ...    Applicability: none
    ...    Post-Conditions: the resource is in NOT_INSTANTIATED state
    Check resource existence
    Check resource instantiated
    POST Terminate NSInstance
    Check HTTP Response Status Code Is    202
    Check Operation Occurrence Id
    Check Operation Notification Status is    START
    Check Operation Notification Status is    RESULT
    Check resource not_instantiated
    
    
    
    
    
    
    
    
    
    
    