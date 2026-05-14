import requests
import json
import time
import logging

from rich.table import Table
from rich.live import Live

base_url = "https://opendata.adsb.fi/api/"
west_Turkey = "/v3/lat/40.0/lon/29.0/dist/250"
middle_Turkey = "/v3/lat/38.5/lon/34.0/dist/250"
east_Turkey = "/v3/lat/39.0/lon/41.0/dist/250"


class JSONLOG(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, 'anomalies'):
            log_record["flight"] = record.anomalies[0].get("flight", 'N/A')
            log_record["description"] = record.anomalies[0].get("description", 'N/A')
            log_record["latitude"] = record.anomalies[0].get("latitude", 'N/A')
            log_record["longitude"] = record.anomalies[0].get("longitude", 'N/A')
            log_record["ground_speed"] = record.anomalies[0].get("ground_speed", 'N/A')
            log_record["anomaly_reason"] = record.anomalies[1]

        return json.dumps(log_record)


def get_logger():
    logger = logging.getLogger("anomaly_logger")
    if not logger.handlers:

    
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("anomalies.json",encoding='utf-8')
        handler.setFormatter(JSONLOG())
        logger.addHandler(handler)
    return logger


def api_request():
    try:
        west = requests.get(f"{base_url}{west_Turkey}").json()['ac']
        time.sleep(1.5)
        middle = requests.get(f"{base_url}{middle_Turkey}").json()['ac']
        time.sleep(1.5)
        east = requests.get(f"{base_url}{east_Turkey}").json()['ac']
        data = west + middle + east
    except requests.RequestException as e:
        logging.error(f"Error fetching API data: {e}")
        data = []
    return data

def generate_table(data):
    table = Table()
    table.add_column("Flight",style="cyan")
    table.add_column("Description",style="magenta")
    table.add_column("R",style="green")
    table.add_column("Altitude",style="yellow")
    table.add_column("Ground Speed",style="blue")
    table.add_column("Track",style="red")


    for plane in data:
        table.add_row(
            str(plane.get("flight", 'N/A')),
            str(plane.get("desc", 'N/A')),
            str(plane.get("r", 'N/A')),
            str(plane.get("alt_baro", 'N/A')),
            str(plane.get("gs", 'N/A')),
            str(plane.get("track", 'N/A'))
        )

    return table

def live_table():
    with Live(generate_table(), refresh_per_second=1) as live:
        while True:
            time.sleep(5)
            live.update(generate_table())



def anomaly_detection(data):
    with open('config.json') as f:
        config = json.load(f)
    speed_threshold = config.get("speed_threshold", 100)
    altitude_threshold = config.get("altitude_threshold", 10000)
    
    anomalies = []

    
    for plane in data:
        plane_features = {
            "flight": plane.get("flight", 'N/A'),
            "description": plane.get("desc", 'N/A'),
            "latitude": plane.get("lat", 'N/A'),
            "longitude": plane.get("lon", 'N/A'),
            "ground_speed": plane.get("gs", 'N/A')
        }

        if plane.get('gs',0) > speed_threshold:
            anomalies.append([plane_features, "speed threshold exceeded"])
        elif plane.get("lat",0) > config.get("lat_max") or plane.get("lat",0) < config.get("lat_min") or plane.get("lon",0) > config.get("lon_max") or plane.get("lon",0) < config.get("lon_min"):
            anomalies.append([plane_features, "Plane not in İstanbul airspace"])
        elif plane.get("seen",0) > config.get("last_signal_threshold"):
            anomalies.append([plane_features, "Plane has not been seen for a 30 seconds"])                                      
        else:
            continue
    
    for anomaly in anomalies:
        get_logger().info("Anomaly detected", extra={"anomalies": anomaly})
        

    return anomalies
