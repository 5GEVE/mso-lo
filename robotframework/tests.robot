*** Settings ***
Resource    environment/variables.txt
Resource   NSLCMOperationKeywords.robot
Library    REST    ${MSO-LO_BASE_API}
Library    OperatingSystem
Library    JSONLibrary
Library    JSONSchemaLibrary    schemas/


*** Test Cases ***

Using 'Evaluate' to find a pattern in a string
    Using 'Evaluate' to find a pattern in a string
