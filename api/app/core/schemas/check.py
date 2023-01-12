#!/usr/bin/env python

import json


def has_type(obj, key=None):
    if isinstance(obj, dict):
        if 'type' not in obj and '$ref' not in obj and key != 'properties':
            raise Exception(f"No type found for '{key}'")
        for k, v in obj.items():
            has_type(v, k)
    elif isinstance(obj, list):
        for v in obj:
            has_type(v)


if __name__ == '__main__':
    with open('./apex_options.json', 'r') as f:
        data = json.load(f)
    has_type(data['properties'], 'properties')
