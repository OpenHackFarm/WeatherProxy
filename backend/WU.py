#!/usr/bin/env python
# encoding: utf-8

'''
https://www.wunderground.com/weather/api/d/docs
'''

import requests

from utils import remap_dict_columns


class WU:
    current_column_map = {
        "latitude": "latitude",
        "longitude": "longitude",
        "city": "city",
        "temp_c": "temperature_c",
        "relative_humidity": "humidity",
        "pressure_mb": "pressure",
        "observation_time_rfc822": "datetime",
        "wind_dir": "wind_direction",
        "wind_kph": "wind_speed"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.url_base = 'http://api.wunderground.com/api/%s/conditions/forecast10day/q/' % self.API_KEY

    # def get_realtime(self, id):
    def get_realtime(self, lat, lng):
        current = {}

        url = self.url_base + '%s,%s.json' % (lat, lng)

        r = requests.get(url)
        r = r.json()['current_observation']
        # return r

        current.update(remap_dict_columns(r, self.current_column_map, drop=True))
        current.update(remap_dict_columns(r['observation_location'], self.current_column_map, drop=True))

        current['wind_speed'] = current['wind_speed'] * 0.27777777777778  # kph to mps
        current['url'] = url

        return current

    def get_forecast(self, lat, lng):
        forecast = {}

        url = self.url_base + '%s,%s.json' % (lat, lng)

        r = requests.get(url)
        r = r.json()['forecast']
        return r
