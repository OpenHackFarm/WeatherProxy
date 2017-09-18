#!/usr/bin/env python
# encoding: utf-8


class WeatherProxy(object):
    def __new__(self, backend):
        mod = __import__('backend.' + backend, fromlist=[backend])
        return getattr(mod, backend)()
