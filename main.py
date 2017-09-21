#!/usr/bin/env python
# encoding: utf-8

import argparse

from WeatherProxy import WeatherProxy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--backend', type=str)
    parser.add_argument('--get', dest='query', choices=['realtime', 'forecast', 'towns'], default='realtime')
    parser.add_argument('--id', type=str)
    parser.add_argument('--dataset', type=str)
    parser.add_argument('--town_index', type=str)

    args = parser.parse_args()

    w = WeatherProxy(args.backend)

    if args.dataset and args.town_index:
        print getattr(w, 'get_' + args.query)(args.dataset, args.town_index)
    elif args.id:
        print getattr(w, 'get_' + args.query)(args.id)
    else:
        print getattr(w, 'get_' + args.query)()
