#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests
import json

from utils import remap_dict_columns


class CWB_OA:
    realtime_column_map = {
        "rainfall": "rain",
        "temperature": "temp_c",
        "felt_air_temp": "felt_temp_c",
        "humidity": 'humidity',
        "sunset": "sunset",
        "at": "datetime",
        "sunrise": "sunrise",
        "desc": "condition",
        "specials": "specials"
    }

    def get_realtime(self, id):
        r = requests.get('https://works.ioa.tw/weather/api/weathers/%s.json' % str(id))

        return json.dumps([remap_dict_columns(r.json(), self.realtime_column_map, drop=True)])

    def get_forecast(self):
        pass

    def get_towns(self):
        r = requests.get('https://raw.githubusercontent.com/OpenHackFarm/works.ioa.tw/master/towns.json')

        return json.dumps(r.json())
