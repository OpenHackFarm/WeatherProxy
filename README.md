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
```
$ python main.py --backend 'CWB_OA' --id 57
```

Turn into RESTful API
---
```
$ python cli2restful.py --run python main.py
```
