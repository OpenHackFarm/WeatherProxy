README
===

Use Library
---

```
from WeatherProxy import WeatherProxy

w = WeatherProxy('CWB_OA')

print w.get_current( **{"id": 57} )
```

Run in command line
---
Get current weather
```
$ python main.py --backend 'CWB_OA' --q '{"id": 57}'
```

Get forecast
```
$ python main.py --backend CWB --get forecast --q '{"dataset": "F-D0047-003", "town_index": 9}'
```

Turn into RESTful API
---
```
$ python cli2restful.py --run python main.py
```

```
$ gunicorn -b 0.0.0.0:8001 'cli2restful:main(run="python main.py")'
```

```
# All
http://127.0.0.1:8001/?backend=CWB_with_OA&get=weather_demo

# Current
http://127.0.0.1:8001/?backend=CWB_OA&q={"id":57}
http://127.0.0.1:8001/?backend=OWM&key=YOUR_KEY_HERE&q={"address":"小間書菜"}
http://localhost:8001/?backend=WU&key=YOUR_KEY_HERE&q={"address":"小間書菜"}
http://localhost:8001/?backend=ForecastIO&key=YOUR_KEY_HERE&q={"address":"小間書菜"}

# Forecast
http://127.0.0.1:8001/?backend=CWB&get=forecast&q={"dataset":"F-D0047-003","town_index":9}

# Town & Towns
http://127.0.0.1:8001/?backend=CWB_OA&get=towns
```
