#!/usr/bin/env python
# encoding: utf-8

import sys
import requests

KEY = "eEabxujMEXil4kmoPwzbLjTAnN9tuUtr"


def address2latlng(address):
    url = "http://open.mapquestapi.com/geocoding/v1/address?key=" + KEY + "&location=" + address

    r = requests.get(url)

    ajson = r.json()

    if (len(ajson["results"]) == 1):
        ret_json = {}
        ret_json['status'] = 'success'
        ret_json['data'] = {'lat': ajson["results"][0]["locations"][0]["latLng"]["lat"], 'lng': ajson["results"][0]["locations"][0]["latLng"]["lng"]}
        return ret_json
    else:
        ret_json = {}
        ret_json['status'] = 'error'
        return ret_json

if __name__ == '__main__':
    print(address2latlng(sys.argv[1]))
