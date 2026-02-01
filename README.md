# Adap1Status - Home Assistant Integráció

Ez egy egyedi Home Assistant integráció az ADA-P1 Mérő eszközhöz. HTTP-n keresztül kéri le az eszköz státusz információit JSON formátumban és jeleníti meg azokat szenzorként a Home Assistant-ben.

## Jellemzők

- Automatikus felismerés és beállítás a felhasználói felületen keresztül
- Valós idejű szenzor adatok:
  - **Szöveges szenzorok**: OS verzió, helyi IP, hostnév, SSID, MQTT szerver, működési idő
  - **Numerikus szenzorok**: WiFi RSSI, WiFi csatorna, soros port aktivitás, működési idő másodpercekben, memória adatok (heap total/free/min free/max alloc/fragmentation), fájlrendszer adatok (total/used), watchdog információk, CPU magok, ACK elemek
  - **Bináris szenzorok**: MQTT kapcsolat, Telegram URL mód/beállítás, szabályok betöltve, watchdog engedélyezve
- Konfigurálható lekérdezési időköz (alapértelmezett: 30 másodperc, 10-300 másodperc között állítható)
- Helyi lekérdezés - nincs szükség felhő kapcsolatra
- Átfogó hiba- és kivételkezelés
- Eszköz információk és azonosítók a több eszköz támogatásához
  

  <img width="457" height="720" alt="kép" src="https://github.com/user-attachments/assets/afe28a30-e86f-449f-bf8d-7a7b165d0510" />


## Telepítés

### Manuális telepítés

1. Másold a `custom_components/adap1status` mappát a Home Assistant `custom_components` könyvtárába
2. Indítsd újra a Home Assistant-et
3. Add hozzá az integrációt a felhasználói felületen keresztül:
   - Menj a Beállítások → Eszközök és szolgáltatások menüpontba
   - Kattints a "+ Integráció hozzáadása" gombra
   - Keress rá az "Adap1Status" kifejezésre
   - Add meg az ADA-P1 Mérő eszköz kapcsolódási adatait:
     - **Host**: IP cím vagy hostnév (pl.: `192.168.1.100`)
     - **Port**: Port szám (alapértelmezett: `8989`)
     - **Név**: Opcionális egyedi név az eszközhöz

### HACS telepítés

Ez az integráció hozzáadható a HACS-hez egyedi repository-ként:

1. Nyisd meg a HACS-t a Home Assistant-ben
2. Kattints a három pontra a jobb felső sarokban
3. Válaszd az "Egyedi repository-k" opciót
4. Add hozzá ezt a repository-t: `https://github.com/Iminet72/adaP1Status`
5. Válaszd az "Integration" kategóriát
6. Telepítsd az integrációt
7. Indítsd újra a Home Assistant-et

## Beállítás

### Alapértelmezett beállítás

Az integráció a Home Assistant felhasználói felületén keresztül konfigurálható. A következő adatokat kell megadnod:

- **Host** (kötelező): Az ADA-P1 Mérő eszköz IP címe vagy hostneve
- **Port** (opcionális): A port szám, alapértelmezett: 8989
- **Név** (opcionális): Egyedi név az eszközhöz, alapértelmezetten "ADA-P1 Meter (host)" lesz

### Opciók beállítása

Az integráció hozzáadása után további opciókat állíthatsz be:

1. Menj a Beállítások → Eszközök és szolgáltatások menüpontba
2. Keresd meg az Adap1Status integrációt
3. Kattints az "Opciók" gombra
4. Állítsd be:
   - **Lekérdezési időköz**: Milyen gyakran kérdezze le az eszközt (10-300 másodperc, alapértelmezett: 30)

## Létrehozott entitások

A sikeres beállítás után a következő entitások jönnek létre:

### Szöveges szenzorok
- `sensor.ada_p1_meter_os_version` - Operációs rendszer verziója
- `sensor.ada_p1_meter_local_ip` - Helyi IP cím
- `sensor.ada_p1_meter_hostname` - Hostnév
- `sensor.ada_p1_meter_ssid` - WiFi hálózat neve (SSID)
- `sensor.ada_p1_meter_mqtt_server` - MQTT szerver címe
- `sensor.ada_p1_meter_uptime_hhmm` - Működési idő (ÓÓ:PP formátumban)

### Numerikus szenzorok
- `sensor.ada_p1_meter_wifi_rssi` - WiFi jelerősség (dBm)
- `sensor.ada_p1_meter_wifi_channel` - WiFi csatorna
- `sensor.ada_p1_meter_serial_recent` - Utolsó soros port aktivitás (másodperc)
- `sensor.ada_p1_meter_uptime` - Működési idő (másodpercben)
- `sensor.ada_p1_meter_heap_total` - Teljes memória (byte)
- `sensor.ada_p1_meter_heap_free` - Szabad memória (byte)
- `sensor.ada_p1_meter_heap_min_free` - Minimális szabad memória (byte)
- `sensor.ada_p1_meter_heap_max_alloc` - Maximális allokált memória (byte)
- `sensor.ada_p1_meter_heap_fragmentation` - Memória fragmentáció (%)
- `sensor.ada_p1_meter_filesystem_total` - Teljes fájlrendszer méret (byte)
- `sensor.ada_p1_meter_filesystem_used` - Használt fájlrendszer méret (byte)
- `sensor.ada_p1_meter_watchdog_last_kick` - Watchdog utolsó aktiválás (milliszekundum)
- `sensor.ada_p1_meter_chip_cores` - CPU magok száma
- `sensor.ada_p1_meter_ack_items` - ACK elemek száma

### Bináris szenzorok
- `binary_sensor.ada_p1_meter_mqtt_connected` - MQTT kapcsolat állapota
- `binary_sensor.ada_p1_meter_telegram_url_mode` - Telegram URL mód
- `binary_sensor.ada_p1_meter_telegram_url_set` - Telegram URL beállítva
- `binary_sensor.ada_p1_meter_rules_loaded` - Szabályok betöltve
- `binary_sensor.ada_p1_meter_watchdog_enabled` - Watchdog engedélyezve

## API követelmények

Az integráció az ADA-P1 Mérő eszköztől a következő API végpontot várja:

- **Végpont**: `http://{host}:{port}/status`
- **Módszer**: GET
- **Időtúllépés**: 5 másodperc
- **Formátum**: JSON
- **Autentikáció**: Nem szükséges (helyi hálózaton)

### Példa JSON válasz

```json
{
  "os_version": "1.2.3",
  "local_ip": "192.168.1.100",
  "hostname": "ada-p1-meter",
  "ssid": "MyWiFi",
  "mqtt_server": "192.168.1.10",
  "mqtt_connected": true,
  "uptime_hhmm": "12:34",
  "uptime_seconds": 45240,
  "wifi_rssi": -65,
  "wifi_channel": 6,
  "serial_recent_sec": 5,
  "heap_total": 327680,
  "heap_free": 123456,
  "heap_min_free": 100000,
  "heap_max_alloc": 98304,
  "heap_fragmentation": 15,
  "fs_total": 1048576,
  "fs_used": 524288,
  "watchdog_enabled": true,
  "watchdog_last_kick_ms": 100,
  "telegram_url_mode": false,
  "telegram_url_set": true,
  "rules_loaded": true,
  "chip_cores": 2,
  "ack_items": 0
}
```

## Hiba- és kivételkezelés

### Kapcsolódási problémák

Ha az integráció nem tud csatlakozni az eszközhöz:
- Az összes entitás "Nem elérhető" (Unavailable) állapotba kerül
- A logokban hibaüzenet jelenik meg
- Az integráció továbbra is próbálkozik a beállított időközönként

### HTTP hibák

- **HTTP 404/500**: Az entitások "Nem elérhető" állapotba kerülnek
- **Időtúllépés**: 5 másodperc után az entitások "Nem elérhető" állapotba kerülnek
- **JSON parse hiba**: Hibaüzenet a logokban, entitások "Nem elérhető" állapotba kerülnek

### Hiányzó adatok

Ha egy adott mező hiányzik a JSON válaszból:
- Az adott szenzor `None` értéket jelez
- A többi szenzor továbbra is működik

## Hibaelhárítás

### Az integráció nem jelenik meg a listában

- Ellenőrizd, hogy a fájlok a megfelelő helyre kerültek-e
- Indítsd újra a Home Assistant-et
- Nézd meg a Home Assistant logokat az `adap1status`-hoz kapcsolódó hibák után

### Nem lehet csatlakozni az eszközhöz

- Ellenőrizd a host és port beállításokat
- Győződj meg róla, hogy az eszköz be van kapcsolva és csatlakozik a hálózathoz
- Próbáld elérni a `http://{host}:{port}/status` URL-t egy böngészőből
- Ellenőrizd a hálózati tűzfal beállításokat

### A szenzorok "Ismeretlen" vagy "Nem elérhető" állapotúak

- Ellenőrizd az eszköz URL elérhetőségét
- Nézd meg az eszköz JSON választ böngészőből
- Ellenőrizd a Home Assistant logokat részletes hibaüzenetek után

### Logok megtekintése

Részletes logokhoz adj hozzá a `configuration.yaml` fájlhoz:

```yaml
logger:
  default: info
  logs:
    custom_components.adap1status: debug
```

Ezután indítsd újra a Home Assistant-et és nézd meg a logokat.

## Ismert korlátok

- Az integráció csak HTTP-t támogat, HTTPS-t nem (helyi hálózati használatra tervezve)
- Nincs autentikáció támogatás
- A JSON válasznak pontosan a megadott formátumnak kell megfelelnie
- Minimum Home Assistant 2023.1.0 verzió szükséges

## Követelmények

- Home Assistant 2023.1.0 vagy újabb
- ADA-P1 Mérő eszköz HTTP-n keresztül elérhető
- Hálózati kapcsolat a Home Assistant és az eszköz között
- Python 3.11 vagy újabb (Home Assistant követelmény)

## Támogatás

Problémák, kérdések vagy funkció kérések esetén használd a [GitHub Issues](https://github.com/Iminet72/adaP1Status/issues) oldalt.

## Licenc

Ez az integráció "ahogy van" alapon kerül kiadásra, mindenféle garancia nélkül. Lásd a LICENSE fájlt részletekért.

## Fejlesztés

Ha szeretnél hozzájárulni a projekthez, kérlek nézd meg a [CONTRIBUTING.md](CONTRIBUTING.md) fájlt.

## Változások

A részletes változások listáját lásd a [CHANGELOG.md](CHANGELOG.md) fájlban.
