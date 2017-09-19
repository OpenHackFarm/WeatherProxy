#!/usr/bin/env python
# encoding: utf-8

'''
https://works.ioa.tw/weather/api/doc/index.html
'''

import requests
import json


class CWB_OA:
    def get_realtime(self, id):
        r = requests.get('https://works.ioa.tw/weather/api/weathers/%s.json' % str(id))

        return json.dumps(r.json())

    def get_forecast(self):
        pass

    def get_towns(self):
        return 'Check https://github.com/OpenHackFarm/works.ioa.tw'
