import json

f = open('CWB_Stations_171226.json')
stations = json.load(f)

for s in stations:
    print("INSERT INTO `weather_stations` (`source`, `station_id`, `name`, `city`, `address`, `lat`, `lng`, `alt`, `start_date`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % ('CWB', s['站號'], s['站名'], s['城市'], s['地址'], s['緯度'], s['經度'], s['海拔高度(m)'], s['資料起始日期']))
