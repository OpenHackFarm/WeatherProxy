#!/usr/bin/env python
# encoding: utf-8

'''
Dataset
https://opendata.cwb.gov.tw/datalist


How to use cwb-cache library:
---------------------------------------------------------------
$ cd thirdparty/
$ git clone https://github.com/leafwind/cwb-cache.git
$ echo "AUTH_KEY = 'YOUR_AUTH_KEY'" > cwb-cache/cwb_auth_key.py
---------------------------------------------------------------
'''

import sys
sys.path.append('thirdparty/cwb-cache')

from forecast_36hr import get_data_from_cwb, AUTH_KEY

from utils import remap_dict_columns


class CWB:
    forecast_column_map = {
        "WeatherDescription": "description",
        "RH": "humidity",
        "MaxT": "max_temp_c",
        "MinT": "min_temp_c"
    }

    @property
    def get_realtime(self):
        return "CWB Realtime data."

    def get_forecast(self, dataset_id, town_index):
        forecast_dict = {}
        forecast_list = []

        json_object = get_data_from_cwb(dataset_id, AUTH_KEY, {})

        for i in json_object['records']['locations'][0]['location'][int(town_index)]['weatherElement']:
            if i['elementName'] in ['MinT', 'MaxT', 'RH', 'PoP', 'WeatherDescription']:
                for j in i['time']:
                    if j['startTime'] + '-' + j['endTime'] not in forecast_dict:
                        forecast_dict[j['startTime'] + '-' + j['endTime']] = {}
                        forecast_dict[j['startTime'] + '-' + j['endTime']]['start_time'] = j['startTime']
                        forecast_dict[j['startTime'] + '-' + j['endTime']]['end_time'] = j['endTime']

                    forecast_dict[j['startTime'] + '-' + j['endTime']][i['elementName']] = j['elementValue']

        forecast_list = []
        for forecast in sorted(forecast_dict.items()):
            forecast_list.append(remap_dict_columns(forecast[1], self.forecast_column_map))

        return [forecast_list]
