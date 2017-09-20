#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests

from utils import remap_column


class CWB_OA:
    realtime_column_map = {
        "rainfall": "rain",
        "temperature": "temp_c",
        "felt_air_temp": "felt_temp_c",
        "humidity": 'humidity',
        "sunset": "sunset",
        "at": "datetime",
        "sunrise": "sunrise",
        "desc": "condition"
    }

    def get_realtime(self, id):
        r = requests.get('https://works.ioa.tw/weather/api/weathers/%s.json' % str(id))

        return remap_column(r.json(), self.realtime_column_map)

    def get_forecast(self):
        pass

    def get_towns(self):
        return 'Check https://github.com/OpenHackFarm/works.ioa.tw'
