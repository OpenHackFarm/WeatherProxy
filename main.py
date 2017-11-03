#!/usr/bin/env python
# encoding: utf-8

import argparse

from WeatherProxy import WeatherProxy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--backend', type=str)
    parser.add_argument('--key', type=str)
    parser.add_argument('--get', dest='query', choices=['weather_demo', 'current', 'forecast', 'town', 'towns', 'stations'], default='current')
    parser.add_argument('--q', dest='query_string', type=str)

    args = parser.parse_args()

    w = WeatherProxy(args.backend, args.key)

    if args.query_string:
        print getattr(w, 'get_' + args.query)(**eval(args.query_string))
    else:
        print getattr(w, 'get_' + args.query)()
