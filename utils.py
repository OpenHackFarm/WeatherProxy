#!/usr/bin/env python
# encoding: utf-8

import json


def json2dict(rows):
    try:
        if type(rows) != dict:
            rows = json.loads(rows)
    except Exception:
        pass

    return rows


def remap_column(rows, name_map):
    new_rows = {}

    rows = json2dict(rows)

    for k, v in rows.iteritems():
        if k in name_map.keys():
            new_rows[name_map[k]] = v

    return json.dumps(new_rows)
