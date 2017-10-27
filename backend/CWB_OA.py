#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests
import os.path
import json
from scipy import spatial

from utils import remap_dict_columns, measure_distance


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

    def get_current(self, id):
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
        _ = None
        if os.path.isfile('thirdparty/works.ioa.tw/towns.json'):
            with open('thirdparty/works.ioa.tw/towns.json') as json_data:
                _ = json.load(json_data)
        else:
            url = 'https://raw.githubusercontent.com/OpenHackFarm/works.ioa.tw/master/towns.json'

            r = requests.get(url)

            _ = r.json()

        towns = []
        for town in _:
            towns.append(remap_dict_columns(town, self.township_column_map))

        return towns

    def get_stations(self, lat, lng, max_distance=None):
        stations = []

        all_stations = None
        if os.path.isfile('thirdparty/works.ioa.tw/towns.json'):
            with open('thirdparty/works.ioa.tw/towns.json') as json_data:
                all_stations = json.load(json_data)
        else:
            url = 'https://raw.githubusercontent.com/OpenHackFarm/works.ioa.tw/master/towns.json'

            r = requests.get(url)

            all_stations = r.json()

        all_coords = [(float(s['position']['lat']), float(s['position']['lng'])) for s in all_stations]
        # return all_coord[0]

        tree = spatial.KDTree(all_coords)
        nearest = tree.query([(lat, lng)], 10)
        # print nearest[1][0]

        for i in nearest[1][0]:
            if all_stations[i]['position']['lat'] and all_stations[i]['position']['lng']:
                distance_km = measure_distance((lat, lng), (float(all_stations[i]['position']['lat']), float(all_stations[i]['position']['lng'])))
                if max_distance and max_distance < distance_km:
                    pass
                else:
                    all_stations[i]['distance_km'] = distance_km
                    # stations.append(remap_dict_columns(all_stations[i], self.station_column_map))
                    stations.append(all_stations[i])

        return stations
