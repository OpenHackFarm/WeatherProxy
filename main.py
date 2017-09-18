#!/usr/bin/env python
# encoding: utf-8

from WeatherProxy import WeatherProxy

if __name__ == '__main__':
    w = WeatherProxy('CWB')
    print w.get_realtime
