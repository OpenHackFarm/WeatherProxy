#!/usr/bin/env python
# encoding: utf-8


class WeatherProxy(object):
    def __new__(self, backend, key=None):
        mod = __import__('backend.' + backend, fromlist=[backend])
        if key:
            return getattr(mod, backend)(key)
        else:
            return getattr(mod, backend)()
