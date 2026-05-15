import requests
import json
import time
import logging
from summarizer import generate_report
from rich.table import Table
from rich.live import Live

base_url = "https://opendata.adsb.fi/api/"
west_Turkey = "/v3/lat/40.0/lon/29.0/dist/250"
middle_Turkey = "/v3/lat/38.5/lon/34.0/dist/250"
east_Turkey = "/v3/lat/39.0/lon/41.0/dist/250"
Greece       = "/v3/lat/39.0/lon/22.0/dist/250"   # Yunanistan, Ege
Romania      = "/v3/lat/44.0/lon/25.0/dist/250"   # Romanya, Bulgaristan
Black_sea    = "/v3/lat/46.5/lon/33.0/dist/250"   # Ukrayna, Kırım
Caucasus     = "/v3/lat/43.0/lon/43.0/dist/250"   # Gürcistan, Ermenistan
Azerbaijan   = "/v3/lat/38.0/lon/50.0/dist/250"   # Azerbaycan, KD İran
Syria        = "/v3/lat/34.0/lon/36.0/dist/250"   # Suriye, Lübnan, Kıbrıs
Iraq         = "/v3/lat/34.0/lon/44.0/dist/250"   # Irak, Batı İran
Egypt        = "/v3/lat/30.0/lon/31.0/dist/250"   # Mısır, Doğu Akdeniz


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
        west_turkey = requests.get(f"{base_url}{west_Turkey}").json()['ac']
        time.sleep(1.5)
        middle_turkey = requests.get(f"{base_url}{middle_Turkey}").json()['ac']
        time.sleep(1.5)
        east_turkey = requests.get(f"{base_url}{east_Turkey}").json()['ac']
        time.sleep(1.5)
        greece       = requests.get(f"{base_url}{Greece}").json()['ac']
        time.sleep(1.5)
        romania      = requests.get(f"{base_url}{Romania}").json()['ac']
        time.sleep(1.5)
        black_sea    = requests.get(f"{base_url}{Black_sea}").json()['ac']
        time.sleep(1.5)
        caucasus     = requests.get(f"{base_url}{Caucasus}").json()['ac']
        time.sleep(1.5)
        azerbaijan   = requests.get(f"{base_url}{Azerbaijan}").json()['ac']
        time.sleep(1.5)
        syria        = requests.get(f"{base_url}{Syria}").json()['ac']
        time.sleep(1.5)
        iraq         = requests.get(f"{base_url}{Iraq}").json()['ac']
        time.sleep(1.5)
        egypt        = requests.get(f"{base_url}{Egypt}").json()['ac']
        data = west_turkey + middle_turkey + east_turkey + greece + romania + black_sea + caucasus + azerbaijan + syria + iraq + egypt
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

def render_table(data):
    table = generate_table(data)
    return table


def load_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

def anomaly_detection(data, config):
    
    anomalies = []

    
    for plane in data:
        plane_features = {
            "flight": plane.get("flight", 'N/A'),
            "description": plane.get("desc", 'N/A'),
            "latitude": plane.get("lat", 'N/A'),
            "longitude": plane.get("lon", 'N/A'),
            "ground_speed": plane.get("gs", 'N/A')
        }

        if plane.get('gs',0) > config.get("speed_threshold"):
            anomalies.append([plane_features, "speed threshold exceeded"])
        if plane.get("lat",0) > config.get("lat_max") or plane.get("lat",0) < config.get("lat_min") or plane.get("lon",0) > config.get("lon_max") or plane.get("lon",0) < config.get("lon_min"):
            anomalies.append([plane_features, "Plane not in Turkish airspace"])
        if plane.get("seen",0) > config.get("last_signal_threshold"):
            anomalies.append([plane_features, "Plane has not been seen for a 30 seconds"])                                      
        else:
            continue
    
    for anomaly in anomalies:
        get_logger().info("Anomaly detected", extra={"anomalies": anomaly})

    return anomalies

def main():
    data = api_request()
    config = load_config()

    with Live(refresh_per_second=1) as live:
        while True:
            data = api_request()
            anomalies = anomaly_detection(data, config)
            live.update(render_table(data))
            time.sleep(4)
    generate_report()

if __name__ == "__main__":
    main()          