README
===

Use Library
---

```
from WeatherProxy import WeatherProxy

w = WeatherProxy('CWB_OA')

print w.get_realtime(57)

```

Run in command line
---
Get current weather
```
$ python main.py --backend 'CWB_OA' --id 57

Get forecast
```
$ python main.py --backend CWB --get forecast --dataset F-D0047-003 --town_index 9
```

Turn into RESTful API
---
```
$ python cli2restful.py --run python main.py
```
