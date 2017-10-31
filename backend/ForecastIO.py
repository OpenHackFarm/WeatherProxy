#!/usr/bin/env python
# encoding: utf-8

'''
https://darksky.net/dev/docs

https://github.com/damian-w/forecast.io-javascript-jsonp-api/blob/master/src/main.js
'''

import requests
from datetime import datetime

import pytemperature
from utils import remap_dict_columns


class ForecastIO:
    current_column_map = {
        "temperature": "temperature_c",
        "summary": "condition",
        "windSpeed": "wind_speed",
        "windBearing": "wind_degrees",
        "humidity": "humidity",
        "pressure": "pressure",
        "visibility": "visibility",
        "time": "datetime",
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.url_base = 'https://api.darksky.net/forecast/%s/' % self.API_KEY

    def get_current(self, lat, lng):
        current = {}

        url = self.url_base + '%s,%s' % (lat, lng)

        r = requests.get(url)
        r = r.json()

        current.update(remap_dict_columns(r['currently'], self.current_column_map, drop=True))
        current.update({'url': url})

        current['temperature_c'] = round(pytemperature.f2c(current['temperature_c']), 2)
        current['humidity'] = current['humidity'] * 100
        current['datetime'] = datetime.fromtimestamp(current['datetime']).strftime("%Y-%m-%d %H:%M:%S")

        return current

    @property
    def get_forecast(self):
        return "Forecast.io Forecast data."
