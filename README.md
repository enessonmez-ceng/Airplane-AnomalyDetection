# ADS-B Flight Anomaly Monitor

Real-time flight tracking and anomaly detection system for Turkish airspace and surrounding regions, using live ADS-B data from the [adsb.fi](https://opendata.adsb.fi) open API.

## Overview

The system continuously polls ADS-B transponder data from 11 geographic zones covering Turkey, Greece, the Black Sea, the Caucasus, and the Middle East. It detects suspicious or out-of-bounds aircraft behavior, logs anomalies to a structured JSON file, and generates an HTML report every 30 minutes.

## Project Structure

```
├── main.py               # Entry point — fetches data, runs live dashboard, detects anomalies
├── summarizer.py         # Report generator — reads anomaly log and renders HTML report
├── report_template.html  # Jinja2 template for the HTML anomaly report
├── config.json           # Thresholds and airspace boundaries
└── requirements.txt      # Python dependencies
```

## Features

- **Live terminal dashboard** — scrolling table of all aircraft in range, updated every cycle via [Rich](https://github.com/Textualize/rich)
- **Anomaly detection** — flags aircraft that exceed speed limits, leave defined airspace, or go silent
- **Structured JSON logging** — each anomaly is appended as a JSON line to `anomalies.json`
- **Automatic HTML reports** — generated every 30 minutes using the Jinja2 template

## Anomaly Rules

Defined in `config.json`:

| Rule | Field | Default |
|---|---|---|
| Speed threshold | `speed_threshold` | 100 knots |
| Latitude bounds | `lat_min` / `lat_max` | 35.8 – 42.2 |
| Longitude bounds | `lon_min` / `lon_max` | 26.0 – 44.8 |
| Signal timeout | `last_signal_threshold` | 30 seconds |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The program runs indefinitely. Press `Ctrl+C` to stop. Reports are saved as `report.html` and anomalies are logged to `anomalies.json`.

## Configuration

Edit `config.json` to adjust detection thresholds:

```json
{
    "speed_threshold": 100,
    "lat_max": 42.2,
    "lat_min": 35.8,
    "lon_max": 44.8,
    "lon_min": 26.0,
    "last_signal_threshold": 30
}
```

## Data Source

[adsb.fi](https://opendata.adsb.fi) — free, community-driven ADS-B aggregator. No API key required.
