import json
import datetime as dt
with open("kanji.json", "r", encoding="utf-8") as f:
    kanji_u2 = json.load(f)
d1 = dt.datetime.now().time()
d2 = dt.datetime.strptime(kanji_u2[str("483317936862527499")]["time"], '%H:%M:%S').time()
print(type(d2))
print(type(d1))
d3 = dt.timedelta(d1) - dt.timedelta(d2)
print(d3)