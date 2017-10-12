#!/usr/bin/env python
# encoding: utf-8

import json
from math import radians, cos, sin, asin, sqrt


def json2dict(rows):
    try:
        if type(rows) != dict:
            rows = json.loads(rows)
    except Exception:
        pass

    return rows


def remap_dict_columns(rows, name_map, drop=False):
    new_rows = {}

    rows = json2dict(rows)

    for k, v in rows.iteritems():
        if k in name_map.keys():
            new_rows[name_map[k]] = v
        else:
            # keep origin key
            if drop is False:
                new_rows[k] = v

    return new_rows


def measure_distance(coord_1, coord_2):  # (42.057, -71.08), (39.132, -84.5155)
    lat1 = coord_1[0]
    lon1 = coord_1[1]
    lat2 = coord_2[0]
    lon2 = coord_2[1]
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    # return c * r * 1000
    return round(c * r, 2)
