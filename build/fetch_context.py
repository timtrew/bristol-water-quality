"""Download daily rainfall (Open-Meteo archive) and OpenStreetMap waterways for Bristol.

Writes rain.json and waterways.json next to this script. Run fetch_cso.py for spill data,
then build_data.py to rebuild ../data.js.
"""
import datetime as dt
import json
import urllib.parse
import urllib.request

end = (dt.date.today() - dt.timedelta(days=2)).isoformat()
rain_url = ("https://archive-api.open-meteo.com/v1/archive?latitude=51.455&longitude=-2.59"
            "&start_date=1994-01-01&end_date=" + end + "&daily=precipitation_sum&timezone=Europe%2FLondon")
with urllib.request.urlopen(rain_url) as r:
    open("rain.json", "wb").write(r.read())
print("rain.json to", end)

query = ('[out:json][timeout:120];('
         'way["waterway"~"^(river|canal|stream)$"](51.39,-2.74,51.54,-2.44);'
         'way["natural"="water"]["name"](51.39,-2.74,51.54,-2.44););out geom;')
req = urllib.request.Request("https://overpass-api.de/api/interpreter",
                             data=urllib.parse.urlencode({"data": query}).encode(),
                             headers={"User-Agent": "bristol-water-quality-app", "Accept": "*/*"})
with urllib.request.urlopen(req) as r:
    w = json.load(r)
json.dump(w, open("waterways.json", "w"))
print("waterways.json", len(w["elements"]), "features")
