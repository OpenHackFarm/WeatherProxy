#!/usr/bin/env python
# encoding: utf-8

'''
csparpa/pyowm
https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md

```
# pip install pyown
```
'''

import pyowm
import json

import pytemperature
from utils import remap_dict_columns


class OWM:
    realtime_column_map = {
        "temp": "temp_c",
        "humidity": "humidity",
        "detailed_status": "condition",
        "press": "pressure",
        "sunset_time": "sunset",
        "sunrise_time": "sunrise"
    }

    def __init__(self, API_KEY):
        self.owm = pyowm.OWM(API_KEY)

    def get_realtime(self, lat, lon):
        realtime = {}

        obs = self.owm.weather_at_coords(lat, lon)
        response = obs.get_weather().to_JSON()

        realtime = remap_dict_columns(json.loads(response), self.realtime_column_map, drop=True)
        realtime.update(remap_dict_columns(json.loads(response)['temperature'], self.realtime_column_map, drop=True))
        realtime.update(remap_dict_columns(json.loads(response)['pressure'], self.realtime_column_map, drop=True))

        realtime['temp_c'] = round(pytemperature.k2c(realtime['temp_c']), 2)

        return json.dumps([realtime])

    def get_forecast(self, dataset_id, town_index):
        pass
