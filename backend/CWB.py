#!/usr/bin/env python
# encoding: utf-8

'''
https://opendata.cwb.gov.tw/datalist
'''

import json

import sys
sys.path.append('thirdparty/cwb-cache')

from forecast_36hr import get_data_from_cwb, AUTH_KEY


class CWB:
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
            forecast_list.append(forecast[1])

        return json.dumps(forecast_list)
