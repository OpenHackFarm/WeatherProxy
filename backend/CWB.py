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
        "T": "temperature_c",
        "MaxT": "max_temperature_c",
        "MinT": "min_temperature_c",
        "Wx": "condition"
    }

    @property
    def get_realtime(self):
        return "CWB Realtime data."

    def get_forecast(self, dataset_id, town_index):
        forecast_dict = {}
        forecast_list = []

        json_object = get_data_from_cwb(dataset_id, AUTH_KEY, {})
        # return json_object

        for i in json_object['records']['locations'][0]['location'][int(town_index)]['weatherElement']:
            if i['elementName'] in ['MinT', 'MaxT', 'RH', 'PoP', 'WeatherDescription', 'Wx', 'Wind', 'T', 'UVI']:
                for j in i['time']:
                    new_time = j['startTime'] + '-' + j['endTime']
                    if new_time not in forecast_dict:
                        forecast_dict[new_time] = {}
                        forecast_dict[new_time]['start_time'] = j['startTime']
                        forecast_dict[new_time]['end_time'] = j['endTime']

                    if i['elementName'] == 'Wx':
                        forecast_dict[new_time]['condition_code'] = j['parameter'][0]['parameterValue']

                    if i['elementName'] == 'Wind':
                        for _ in j['parameter']:
                            if _['parameterName'] == u'風向縮寫':
                                forecast_dict[new_time]['wind_direction'] = _['parameterValue']
                            elif _['parameterName'] == u'風速':
                                forecast_dict[new_time]['wind_speed'] = _['parameterValue']
                    elif i['elementName'] == 'UVI':
                        for _ in j['parameter']:
                            if _['parameterName'] == u'紫外線指數':
                                forecast_dict[new_time]['UVI'] = _['parameterValue']
                    else:
                        forecast_dict[new_time][i['elementName']] = j['elementValue']

        forecast_list = []
        for forecast in sorted(forecast_dict.items()):
            forecast_list.append(remap_dict_columns(forecast[1], self.forecast_column_map))

        return forecast_list
