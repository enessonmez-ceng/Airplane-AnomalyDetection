from jinja2 import Environment, FileSystemLoader
from datetime import datetime

import json
from collections import Counter

def generate_report():
    records = []
    with open('anomalies.json', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))


    # 1. Jinja2 ortamını kur ve şablonların olduğu klasörü göster (şu anki klasör: '.')
    env = Environment(loader=FileSystemLoader('.'))
    sablon = env.get_template('report_template.html')

    total = len(records)
    reasons = Counter(r['anomaly_reason'] for r in records)


    # 2. Rapor için verileri hazırla (Listeler, sözlükler kullanabilirsin)
    rapor_verisi = {
        "baslik": "Flight Report",
        "tarih": datetime.now().strftime("%d.%m.%Y"),
        "anomalies": records,
        "total_anomalies": total,
        "speed_anomalies": reasons.get("speed threshold exceeded", 0),
        "location_anomalies": reasons.get("Plane not in Turkish airspace", 0),
        "signal_anomalies": reasons.get("Plane has not been seen for a 30 seconds", 0)
    }

    # 3. Şablonu verilerle "Render" et (birleştir)
    sonuc_html = sablon.render(rapor_verisi)

    # 4. Çıktıyı dosyaya yaz
    with open('dinamik_rapor.html', 'w', encoding='utf-8') as f:
        f.write(sonuc_html)

    print("Dinamik rapor oluşturuldu!")