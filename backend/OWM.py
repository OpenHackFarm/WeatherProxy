#!/usr/bin/env python
# encoding: utf-8

'''
https://openweathermap.org/api
'''

import requests
import json

import pytemperature
from utils import remap_dict_columns


class OWM:
    realtime_column_map = {
        "main": "condition",
        "temp": "temp_c",
        "humidity": "humidity",
        "pressure": "pressure",
        "sunset": "sunset",
        "sunrise": "sunrise"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_realtime(self, id):
        realtime = {}

        r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s' % (str(id), self.API_KEY))

        realtime.update(remap_dict_columns(r.json()['weather'][0], self.realtime_column_map, drop=True))
        realtime.update(remap_dict_columns(r.json()['main'], self.realtime_column_map, drop=True))
        realtime.update(remap_dict_columns(r.json()['sys'], self.realtime_column_map, drop=True))
        realtime.update(r.json()['coord'])

        realtime['temp_c'] = round(pytemperature.k2c(realtime['temp_c']), 2)

        return json.dumps([realtime])

    def get_forecast(self, dataset_id, town_index):
        pass
