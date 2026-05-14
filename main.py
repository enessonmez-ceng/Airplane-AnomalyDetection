import requests
import json

base_url = "https://opendata.adsb.fi/api/"
data = requests.get(f"{base_url}v3/lat/41.0082/lon/28.9784/dist/100").json()['ac']

for plane in data:
    print(f"Description: {plane.get('desc')}, Squawk: {plane.get('squawk')}")

with open("planes.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=4)

print("Data saved to planes.json")  