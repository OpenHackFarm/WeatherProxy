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
import json
from scipy import spatial
import requests
from urllib import quote

from forecast_36hr import get_data_from_cwb, AUTH_KEY

from address2latlng import address2latlng
from utils import remap_dict_columns, measure_distance


class CWB:
    # 氣象因子欄位對照表參考 說明資料 連結文件
    # https://opendata.cwb.gov.tw/catalog?group=o&dataid=A0001-001
    # https://opendata.cwb.gov.tw/catalog?group=o&dataid=A0003-001
    current_column_map = {
        "CITY": "city",
        "TOWN": "town",
        "lat": "latitude",
        "lon": "longitude",
        "locationName": "station_name",
        "stationId" : "station_id",
        "obsTime" : "datetime",
        "ELE": "altitude_m",
        "WDIR": "wind_degree",
        "WDSD": "wind_speed_ms",
        "TEMP": "temperature_c",
        "HUMD": "humidity",
        "PRES": "pressure_hPa",
        "SUN": "sunshine_hr",
        "H_24R": "rain_24hr_mm",
        "ELEV": "altitude_m",
        "24R": "rain_24hr_mm",
        "H_UVI": "UVI",
        "D_TX": "max_temperature_c",
        "D_TS": "sunshine_hr"
    }

    forecast_column_map = {
        "WeatherDescription": "description",
        "RH": "humidity",
        "T": "temperature_c",
        "MaxT": "max_temperature_c",
        "MinT": "min_temperature_c",
        "Wx": "condition"
    }

    station_column_map = {
        u"海拔高度(m)": "altitude_m",
        u"地址": "address",
        u"站名": "station_name",
        u"站號": "station_id",
        u"緯度": "latitude",
        u"經度": "longitude",
        u"城市": "city"
    }

    def get_current(self, **kwargs):
        """
        Parameters
        ----------
        name : str
        """
        output_data = {}

        # 查詢自動氣象站
        r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001/?locationName=' + kwargs['name'], headers={"Authorization": AUTH_KEY})
        if len(r.json()['records']['location']) == 0:
            # 查詢局屬氣象站
            r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001/?locationName=' + kwargs['name'], headers={"Authorization": AUTH_KEY})

        if len(r.json()['records']['location']) == 1:
            # print r.json()['records']['location'][0]

            for k, v in r.json()['records']['location'][0].iteritems():
                if type(v) not in [list, dict]:
                    output_data[k] = v

            for w in r.json()['records']['location'][0]['weatherElement']:
                output_data[w['elementName']] = w['elementValue']
            output_data['HUMD'] = str(int(float(output_data['HUMD']) * 100))

            for p in r.json()['records']['location'][0]['parameter']:
                output_data[p['parameterName']] = p['parameterValue']

            for k, v in r.json()['records']['location'][0]['time'].iteritems():
                output_data[k] = v

            return remap_dict_columns(output_data, self.current_column_map, drop=True)
        else:
            return None

    def get_forecast(self, **kwargs):
        """
        Parameters
        ----------
        dataset : str
        town_index : int
        """
        dataset_id = kwargs['dataset']
        town_index = kwargs['town_index']

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

    def get_stations(self, **kwargs):
        """
        Parameters
        ----------
        lat : float
        lng : float

        address : str

        max_distance : float, optional
        """
        if 'address' in kwargs:
            coordinates = address2latlng(kwargs['address'])
            lat = coordinates['data']['lat']
            lng = coordinates['data']['lng']
        else:
            lat = kwargs['lat']
            lng = kwargs['lng']

        max_distance = kwargs['max_distance'] if 'max_distance' in kwargs else None

        stations = []

        with open('data/CWB_Stations.json') as json_data:
            all_stations = json.load(json_data)

        all_coords = [(float(s[u'緯度']), float(s[u'經度'])) for s in all_stations]
        # return all_coord[0]

        tree = spatial.KDTree(all_coords)
        nearest = tree.query([(lat, lng)], 10)
        # print nearest[1][0]

        for i in nearest[1][0]:
            if all_stations[i][u'緯度'] and all_stations[i][u'經度']:
                distance_km = measure_distance((lat, lng), (float(all_stations[i][u'緯度']), float(all_stations[i][u'經度'])))
                if max_distance and max_distance < distance_km:
                    pass
                else:
                    all_stations[i]['source'] = 'CWB'
                    all_stations[i]['current_api'] = u'http://weather-api.openhackfarm.tw/?backend=CWB&get=current&q={"name":"%s"}' % quote(all_stations[i][u'站名'].encode('utf-8'))
                    all_stations[i]['distance_km'] = distance_km
                    stations.append(remap_dict_columns(all_stations[i], self.station_column_map))
                    # stations.append(all_stations[i])

        return stations
