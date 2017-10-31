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

    forecast_column_map = {
        "precipProbability": "PoP",
        "humidity": "humidity",
        "temperatureMin": "min_temperature_c",
        "temperatureMax": "max_temperature_c",
        "icon": "condition",
        "summary": "description",
        "time": "datetime"
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

    def get_forecast(self, lat, lng):
        forecast = []

        url = self.url_base + '%s,%s' % (lat, lng)

        r = requests.get(url)
        # return r.json()
        r = r.json()['daily']['data']
        # return r

        for f in r:
            forecast_dict = {}

            forecast_dict.update(remap_dict_columns(f, self.forecast_column_map, drop=True))

            forecast_dict['min_temperature_c'] = round(pytemperature.f2c(forecast_dict['min_temperature_c']), 2)
            forecast_dict['max_temperature_c'] = round(pytemperature.f2c(forecast_dict['max_temperature_c']), 2)
            forecast_dict['humidity'] = forecast_dict['humidity'] * 100
            forecast_dict['PoP'] = forecast_dict['PoP'] * 100
            forecast_dict['datetime'] = datetime.fromtimestamp(forecast_dict['datetime']).strftime("%Y-%m-%d %H:%M:%S")

            forecast.append(forecast_dict)

        return forecast
