#!/usr/bin/env python
# encoding: utf-8

'''
https://darksky.net/dev/docs

https://github.com/damian-w/forecast.io-javascript-jsonp-api/blob/master/src/main.js
'''

import requests
from datetime import datetime

import pytemperature
from address2latlng import address2latlng
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

    def _fetch_weather_data(self, **kwargs):
        if 'lat' in kwargs and 'lng' in kwargs:
            lat = kwargs['lat']
            lng = kwargs['lng']
        elif 'address' in kwargs:
            coordinates = address2latlng(kwargs['address'])

            lat = coordinates['data']['lat']
            lng = coordinates['data']['lng']
        else:
            return

        url = self.url_base + '%s,%s' % (lat, lng)

        r = requests.get(url)
        r = r.json()

        if r:
            r['url'] = url

        return r

    def get_current(self, **kwargs):
        """
        parameters
        ----------
        lat : float
        lng : float

        address : str
        """
        current = {}

        r = self._fetch_weather_data(**kwargs)

        current.update(remap_dict_columns(r['currently'], self.current_column_map, drop=True))
        current.update({'url': r['url']})

        current['temperature_c'] = round(pytemperature.f2c(current['temperature_c']), 2)
        current['humidity'] = current['humidity'] * 100
        current['datetime'] = datetime.fromtimestamp(current['datetime']).strftime("%Y-%m-%d %H:%M:%S")

        return current

    def get_forecast(self, **kwargs):
        """
        parameters
        ----------
        lat : float
        lng : float

        address : str
        """
        forecast = []

        r = self._fetch_weather_data(**kwargs)
        # return r
        r = r['daily']['data']
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
