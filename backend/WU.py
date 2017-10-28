#!/usr/bin/env python
# encoding: utf-8

'''
https://www.wunderground.com/weather/api/d/docs
'''

import requests

from utils import remap_dict_columns, measure_distance


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

    station_column_map = {
        "lat": "latitude",
        "lon": "longitude"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.url_base = 'http://api.wunderground.com/api/%s/conditions/forecast10day/q/' % self.API_KEY
        self.url_lookup = 'http://api.wunderground.com/api/%s/geolookup/q/' % self.API_KEY

    # def get_current(self, id):
    def get_current(self, lat, lng):
        current = {}

        url = self.url_base + '%s,%s.json' % (lat, lng)

        r = requests.get(url)
        r = r.json()['current_observation']
        # return r

        current.update(remap_dict_columns(r, self.current_column_map, drop=True))
        current.update(remap_dict_columns(r['observation_location'], self.current_column_map, drop=True))

        current['wind_speed'] = current['wind_speed'] * 0.27777777777778  # kph to mps
        current['latitude'] = float(current['latitude'])
        current['longitude'] = float(current['longitude'])
        current['url'] = url
        current['distance'] = measure_distance((lat, lng), (current['latitude'], current['longitude']))

        return current

    def get_forecast(self, lat, lng):
        forecast = []

        url = self.url_base + '%s,%s.json' % (lat, lng)

        r = requests.get(url)
        # return r.json()['forecast']
        r = r.json()['forecast']['simpleforecast']['forecastday']
        # return r

        for f in r:
            forecast_dict = {}
            forecast_dict['condition'] = f['conditions']
            forecast_dict['condition_code'] = f['icon']
            forecast_dict['max_temperature_c'] = f['high']['celsius']
            forecast_dict['min_temperature_c'] = f['low']['celsius']
            forecast_dict['humidity'] = f['avehumidity']
            forecast_dict['PoP'] = f['pop']
            forecast_dict['wind_direction'] = f['avewind']['dir']
            forecast_dict['wind_speed_mph'] = f['avewind']['mph']
            forecast_dict['start_time'] = "%s-%s-%s %s:%s:00" % (f['date']['year'], f['date']['month'], f['date']['day'], f['date']['hour'], f['date']['min'])

            forecast.append(forecast_dict)

        return forecast

    def get_stations(self, lat, lng, max_distance=None):
        stations = []

        url = self.url_lookup + '%s,%s.json' % (lat, lng)

        r = requests.get(url)
        # return r.json()['location']['nearby_weather_stations']

        for s in r.json()['location']['nearby_weather_stations']['airport']['station']:
            if s['lat'] and s['lon']:
                distance_km = measure_distance((lat, lng), (float(s['lat']), float(s['lon'])))
                if max_distance and max_distance < distance_km:
                    pass
                else:
                    s['source'] = 'WU'
                    s['type'] = 'airport'
                    s['distance_km'] = distance_km
                    stations.append(remap_dict_columns(s, self.station_column_map))

        for s in r.json()['location']['nearby_weather_stations']['pws']['station']:
            if s['lat'] and s['lon']:
                distance_km = measure_distance((lat, lng), (float(s['lat']), float(s['lon'])))
                if max_distance and max_distance < distance_km:
                    pass
                else:
                    s['source'] = 'WU'
                    s['type'] = 'pws'
                    s['distance_km'] = distance_km
                    stations.append(remap_dict_columns(s, self.station_column_map))

        return sorted(stations, key=lambda k: int(k['distance_km']))

