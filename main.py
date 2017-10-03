#!/usr/bin/env python
# encoding: utf-8

import argparse
import json

from WeatherProxy import WeatherProxy
from address2latlng import address2latlng

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--backend', type=str)
    parser.add_argument('--key', type=str)
    parser.add_argument('--get', dest='query', choices=['weather_demo', 'realtime', 'forecast', 'town', 'towns'], default='realtime')
    parser.add_argument('--id', type=str)
    parser.add_argument('--dataset', type=str)
    parser.add_argument('--town_index', type=str)
    parser.add_argument('--lat', type=str)
    parser.add_argument('--lon', type=str)
    parser.add_argument('--address', type=str)

    args = parser.parse_args()

    w = WeatherProxy(args.backend, args.key)

    if args.id:
        print getattr(w, 'get_' + args.query)(args.id)
    elif args.address:
        coordinates = json.loads(address2latlng(args.address))
        print getattr(w, 'get_' + args.query)(float(coordinates['data']['lat']), float(coordinates['data']['lng']))
    elif args.lat and args.lon:
        print getattr(w, 'get_' + args.query)(float(args.lat), float(args.lon))
    elif args.dataset and args.town_index:
        print getattr(w, 'get_' + args.query)(args.dataset, args.town_index)
    else:
        print getattr(w, 'get_' + args.query)()
