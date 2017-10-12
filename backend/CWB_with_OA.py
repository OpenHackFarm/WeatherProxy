#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

from CWB import CWB
from CWB_OA import CWB_OA


class CWB_with_OA:
    def __init__(self):
        self.cwb = CWB()
        self.cwb_oa = CWB_OA()

    def get_weather_demo(self):
        return {'current': self.get_realtime('57'),
                'forecast': self.get_forecast('F-D0047-003', '9'),
                'location': self.get_town('57')
                }

    def get_realtime(self, id):
        return self.cwb_oa.get_realtime(id)

    def get_forecast(self, dataset_id, town_index):
        return self.cwb.get_forecast(dataset_id, town_index)

    def get_town(self, id):
        return self.cwb_oa.get_town(id)
