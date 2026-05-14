# ADS-B Veri Alanları Açıklaması

## `hex`
- ICAO 24-bit hexadecimal hava aracı kimliği.
- Her hava aracına özeldir.
- Örnek: `ae1fd9`

---

## `type`
- Verinin kaynağını belirtir.
- `adsb_icao` → Veri doğrudan ADS-B yayınından geliyor.

---

## `flight`
- Callsign / uçuş kodu.
- Hava trafik kontrolünde kullanılan uçuş adı.
- Örnek: `G72202`

---

## `r`
- Aircraft registration (tescil numarası).
- Hava aracının fiziksel kayıt kimliği.
- Örnek: `11-72202`

---

## `t`
- ICAO aircraft type code.
- Kısa model kodu.
- `EC45` → Airbus/Eurocopter EC145 serisi.

---

## `dbFlags`
- Veritabanı veya sistem flag bilgisi.
- Veri kaynağına göre farklı anlamlar taşıyabilir.
- Genellikle:
  - askeri,
  - özel kayıt,
  - ilave metadata
  gibi durumları işaretlemek için kullanılır.

---

## `desc`
- Hava aracının tam model açıklaması.
- Örnek:
  `Airbus Helicopters UH-72A Lakota`

---

## `alt_baro`
- Barometrik irtifa.
- Feet cinsindendir.
- Hava basıncına göre hesaplanır.
- `775` ≈ 236 metre.

---

## `alt_geom`
- GPS/GNSS tabanlı geometrik irtifa.
- Feet cinsindendir.
- `1000` ≈ 304 metre.

---

## `calc_track`
- Hava aracının hareket yönü.
- Derece cinsinden.
- `0` → Kuzey
- `90` → Doğu
- `180` → Güney
- `270` → Batı

`68`
→ Kuzeydoğu yönü.

---

## `category`
- ADS-B hava aracı kategori kodu.

Örnekler:
- `A1` → Hafif uçak
- `A3` → Büyük uçak
- `A5` → Heavy aircraft
- `A7` → Helikopter / rotorcraft

---

## `lat`
- Latitude (enlem).
- Dünya üzerindeki kuzey-güney konumu.

---

## `lon`
- Longitude (boylam).
- Dünya üzerindeki doğu-batı konumu.

---

## `nic`
- Navigation Integrity Category.
- GPS/konum güvenilirliği metriği.
- Yüksek değer → daha güvenilir konum.
- Genellikle 0–11 arasıdır.

---

## `rc`
- Radius of Containment.
- Tahmini konum hata yarıçapı.
- Metre cinsindendir.
- `186` → yaklaşık 186 metre hata payı.

---

## `seen_pos`
- Son konum bilgisinin alınmasından beri geçen süre.
- Saniye cinsindendir.

---

## `version`
- ADS-B protokol versiyonu.
- Genellikle:
  - 0
  - 1
  - 2

`2`
→ daha yeni ADS-B standardı.

---

## `sil_type`
- Source Integrity Level tipi.
- Güvenilirlik ölçüm metodunu belirtir.

`perhour`
→ hata olasılığı saatlik hesaplanıyor.

---

## `alert`
- Acil durum/alarm flagi.
- `0` → normal
- `1` → alarm durumu

---

## `spi`
- Special Position Identification.
- Pilotun IDENT/squawk vurgusu gönderip göndermediğini belirtir.
- `0` → pasif
- `1` → aktif

---

## `mlat`
- Multilateration kaynak bilgileri.
- MLAT tabanlı konumlama kullanıldıysa burada listelenir.
- Boş liste → kullanılmamış.

---

## `tisb`
- Traffic Information Service-Broadcast verileri.
- Yer istasyonlarından gelen trafik bilgileri.
- Boş liste → kullanılmıyor.

---

## `messages`
- Hava aracından alınan toplam ADS-B mesaj sayısı.
- Yüksek sayı → uzun süre takip edilmiş.

---

## `seen`
- Son ADS-B mesajının alınmasından beri geçen süre.
- Saniye cinsindendir.

---

## `rssi`
- Received Signal Strength Indicator.
- Alınan sinyal gücü.
- dB cinsindendir.

Genel yorum:
- Daha az negatif değer → daha güçlü sinyal.

Örnek:
- `-10` → çok güçlü
- `-20` → güçlü
- `-40` → orta
- `-60` → zayıf