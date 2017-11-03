#!/usr/bin/env python
# encoding: utf-8

'''
https://openweathermap.org/api
'''

import requests

import pytemperature
from address2latlng import address2latlng
from utils import remap_dict_columns, measure_distance


class OWM:
    current_column_map = {
        "main": "condition",
        "lat": "latitude",
        "lon": "longitude",
        "temp": "temperature_c",
        "humidity": "humidity",
        "pressure": "pressure",
        "sunset": "sunset",
        "sunrise": "sunrise"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_current(self, **kwargs):
        """
        Parameters
        ----------
        id : int

        lat : float
        lng : float

        address : str
        """
        if 'id' in kwargs:
            id = kwargs['id']

            url = 'http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s' % (id, self.API_KEY)
        elif 'lat' in kwargs and 'lng' in kwargs:
            lat = kwargs['lat']
            lng = kwargs['lng']

            url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s' % (lat, lng, self.API_KEY)
        elif 'address' in kwargs:
            coordinates = address2latlng(kwargs['address'])

            lat = coordinates['data']['lat']
            lng = coordinates['data']['lng']

            url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s' % (lat, lng, self.API_KEY)
        else:
            return

        current = {}

        r = requests.get(url)

        current.update(remap_dict_columns(r.json()['weather'][0], self.current_column_map, drop=True))
        current.update(remap_dict_columns(r.json()['main'], self.current_column_map, drop=True))
        current.update(remap_dict_columns(r.json()['sys'], self.current_column_map, drop=True))
        current.update(remap_dict_columns(r.json()['coord'], self.current_column_map, drop=True))
        current.update({'id': r.json()['id']})
        current.update({'city': r.json()['name']})
        current.update({'url': url})

        current['temperature_c'] = round(pytemperature.k2c(current['temperature_c']), 2)
        if 'lat' in kwargs and 'lng' in kwargs:
            current['distance'] = measure_distance((kwargs['lat'], kwargs['lng']), (current['latitude'], current['longitude']))

        return current

    def get_forecast(self, dataset_id, town_index):
        pass
