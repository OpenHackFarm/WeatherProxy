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
        "temp": "temperature_c",
        "humidity": "humidity",
        "pressure": "pressure",
        "sunset": "sunset",
        "sunrise": "sunrise"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    # def get_realtime(self, id):
    def get_realtime(self, lat, lng):
        realtime = {}

        url = 'http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s' % (str(id), self.API_KEY)
        url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s' % (str(lat), str(lng), self.API_KEY)

        r = requests.get(url)

        realtime.update(remap_dict_columns(r.json()['weather'][0], self.realtime_column_map, drop=True))
        realtime.update(remap_dict_columns(r.json()['main'], self.realtime_column_map, drop=True))
        realtime.update(remap_dict_columns(r.json()['sys'], self.realtime_column_map, drop=True))
        realtime.update(r.json()['coord'])
        realtime.update({'id': r.json()['id']})
        realtime.update({'city': r.json()['name']})

        realtime['temperature_c'] = round(pytemperature.k2c(realtime['temperature_c']), 2)

        return json.dumps([realtime])

    def get_forecast(self, dataset_id, town_index):
        pass
