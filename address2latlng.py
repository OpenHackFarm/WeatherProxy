#!/usr/bin/env python
# encoding: utf-8

# https://gist.github.com/carrl/7148143

import sys
import urllib
import json


def address2latlng(address):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&sensor=false&language=zh-tw"

    res = urllib.urlopen(url)

    ajson = json.load(res)

    res.close()

    if (ajson["status"] == "OK"):
        ret_json = {}
        ret_json['status'] = 'success'
        ret_json['data'] = {'lat': ajson["results"][0]["geometry"]["location"]["lat"], 'lng': ajson["results"][0]["geometry"]["location"]["lng"]}
        return json.dumps(ret_json)
    else:
        ret_json = {}
        ret_json['status'] = 'error'
        return json.dumps(ret_json)

if __name__ == '__main__':
    print(address2latlng(sys.argv[1]))
