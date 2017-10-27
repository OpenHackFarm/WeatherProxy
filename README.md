README
===

Use Library
---

```
from WeatherProxy import WeatherProxy

w = WeatherProxy('CWB_OA')

print w.get_current(57)
```

Run in command line
---
Get current weather
```
$ python main.py --backend 'CWB_OA' --id 57
```

Get forecast
```
$ python main.py --backend CWB --get forecast --dataset F-D0047-003 --town_index 9
```

Turn into RESTful API
---
```
$ python cli2restful.py --run python main.py
```

```
# All
http://127.0.0.1:5000/?backend=CWB_with_OA&get=weather_demo

# Current
http://127.0.0.1:5000/?backend=CWB_OA&id=57
http://127.0.0.1:5000/?backend=OWM&key=YOUR_KEY_HERE&id=1674199

# Forecast
http://127.0.0.1:5000/?backend=CWB&get=forecast&dataset=F-D0047-003&town_index=9

# Town & Towns
http://127.0.0.1:5000/?backend=CWB_OA&get=towns
```
