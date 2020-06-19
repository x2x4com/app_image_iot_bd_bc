#!/usr/bin/env python
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================

from jsonschema import validate, ValidationError

temperature = {
    "type": "object",
    "properties": {
        "time": {
            "type": "string",
            "description": "iso 8661",
            "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}[zZ]?$"
        },
        "value": {"type": "number"},
        "uuid": {
            "type": "string",
            "description": "uuid1 obj",
            "pattern": "^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$"
        },
        "name": {"type": "string"},
    },
    "required": ["time", "value", "uuid", ]
}

iot_log = {
    "type": "object",
    "properties": {
        "time": {
            "type": "string",
            "description": "iso 8661",
            "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}[zZ]?$"
        },
        "log": {
            "type": "string",
            "description": "base64 encoding data"
        },
        "uuid": {
            "type": "string",
            "description": "uuid1 obj",
            "pattern": "^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$"
        },
        "name": {"type": "string"},
    },
    "required": ["time", "log", "uuid", ]
}


def verify_schema(data: dict, schema: dict) -> bool:
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False


def verify_temperature(data: dict) -> bool:
    return verify_schema(data, temperature)


def verify_iot_log(data: dict) -> bool:
    return verify_schema(data, iot_log)

