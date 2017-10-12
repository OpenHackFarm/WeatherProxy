#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests

from utils import remap_dict_columns


class CWB_OA:
    current_column_map = {
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
        current = {}

        url = 'https://works.ioa.tw/weather/api/weathers/%s.json' % str(id)

        r = requests.get(url)

        current = remap_dict_columns(r.json(), self.current_column_map, drop=True)
        current.update({'url': url})

        return current

    def get_forecast(self):
        pass

    def get_town(self, id):
        return [_ for i, _ in enumerate(self.get_towns()) if _['id'] == str(id)][0]

    def get_towns(self):
        url = 'https://raw.githubusercontent.com/OpenHackFarm/works.ioa.tw/master/towns.json'

        r = requests.get(url)

        # return sorted(r.json(), key=lambda k: int(k['id']))

        towns = []
        for town in sorted(r.json(), key=lambda k: int(k['id'])):
            towns.append(remap_dict_columns(town, self.township_column_map))

        return towns
