
id_schema = {"type": "string",
             "pattern": "^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$"}

ns_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "nsInstanceName": {"type": "string"},
        "nsInstanceDescription": {"type": "string"},
        "nsdId": {"type": "string"},
        "nsState": {"type": "string"},
        "vnfInstance": {"type": "array"}
    },
    "required": ["id", "nsInstanceName", "nsInstanceDescription", "nsdId", "nsState"],
    "additionalProperties": False
}


ns_list_schema = {
    "type": "array",
    "items": ns_schema
}

# ?
ns_create_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"}
    },
    "required": ["id"]
}

ns_lcm_op_occ_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "operationState": {"type": "string"},
        "stateEnteredTime": {"type": "string", "format": "date-time"},
        "nsInstanceId": {"type": "string"},
        "lcmOperationType": {"type": "string"},
        "startTime": {"type": "string", "format": "date-time"}
    }
}

ns_lcm_op_occ_list_schema = {
    "type": "array",
    "items": ns_lcm_op_occ_schema
}