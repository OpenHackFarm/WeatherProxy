#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests

from utils import remap_dict_columns


class CWB_OA:
    realtime_column_map = {
        "rainfall": "rain",
        "temperature": "temperature_c",
        "felt_air_temp": "felt_temperature_c",
        "humidity": 'humidity',
        "sunset": "sunset",
        "at": "datetime",
        "sunrise": "sunrise",
        "desc": "condition",
        "specials": "specials"
    }

    township_column_map = {
        "name": "township"
    }

    def get_realtime(self, id):
        r = requests.get('https://works.ioa.tw/weather/api/weathers/%s.json' % str(id))

        return [remap_dict_columns(r.json(), self.realtime_column_map, drop=True)]

    def get_forecast(self):
        pass

    def get_town(self, id):
        return [_ for i, _ in enumerate(self.get_towns()) if _['id'] == str(id)][0]

    def get_towns(self):
        r = requests.get('https://raw.githubusercontent.com/OpenHackFarm/works.ioa.tw/master/towns.json')

        # return sorted(r.json(), key=lambda k: int(k['id']))

        towns = []
        for town in sorted(r.json(), key=lambda k: int(k['id'])):
            towns.append(remap_dict_columns(town, self.township_column_map))

        return towns
