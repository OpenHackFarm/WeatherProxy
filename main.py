#!/usr/bin/env python
# encoding: utf-8

import argparse

from WeatherProxy import WeatherProxy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--backend', type=str)
    parser.add_argument('--key', type=str)
    parser.add_argument('--get', dest='query', choices=['realtime', 'forecast', 'towns'], default='realtime')
    parser.add_argument('--id', type=str)
    parser.add_argument('--dataset', type=str)
    parser.add_argument('--town_index', type=str)
    parser.add_argument('--lat', type=str)
    parser.add_argument('--lon', type=str)

    args = parser.parse_args()

    w = WeatherProxy(args.backend, args.key)

    if args.id:
        print getattr(w, 'get_' + args.query)(args.id)
    elif args.lat and args.lon:
        print getattr(w, 'get_' + args.query)(float(args.lat), float(args.lon))
    elif args.dataset and args.town_index:
        print getattr(w, 'get_' + args.query)(args.dataset, args.town_index)
    else:
        print getattr(w, 'get_' + args.query)()
