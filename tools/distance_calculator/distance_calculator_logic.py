# =============================================================================
# Pouze fce. pro výpočet vzdáleností (bez UI-streamlit)
# =============================================================================

import pandas as pd
import requests
import time
import math
from config import (
    NOMINATIM_URL, NOMINATIM_USER_AGENT,
    NOMINATIM_DELAY_S, NOMINATIM_TIMEOUT_S,
    OSRM_URL_TEMPLATE, OSRM_TIMEOUT_S,
    CSV_COL_FROM_ZIP, CSV_COL_FROM_COUNTRY,
    CSV_COL_TO_ZIP, CSV_COL_TO_COUNTRY,
    CSV_COL_DISTANCE_KM, CSV_COL_STATUS,
    CSV_STATUS_OK, CSV_STATUS_ERROR,
)


# ---------- CACHE ----------
geo_cache = {}

# ---------- FUNKCE ----------

def normalize_postcode(psc):
    return str(psc).zfill(5)


# ✅ GEOCODING (finální verze)
def geocode(postal_code, country):
    postal_code = normalize_postcode(postal_code)
    key = f"{postal_code}_{country}"

    if key in geo_cache:
        return geo_cache[key]

    params = {
        "q": f"{postal_code}, {country}",
        "countrycodes": country.lower(),
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": NOMINATIM_USER_AGENT}

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=NOMINATIM_TIMEOUT_S,
        )
        response.raise_for_status()   # ← chyba pokud HTTP status není 200
        data = response.json()        # ← odděleno od .get()

        if not data:                  # ← prázdný seznam = PSČ nenalezeno
            geo_cache[key] = (None, None)
            return None, None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        geo_cache[key] = (lat, lon)
        return lat, lon

    except Exception:
        geo_cache[key] = (None, None)
        return None, None


# ✅ OSRM vzdalenost (silniční)
def distance_osrm(lat1, lon1, lat2, lon2):
    try:
        url = OSRM_URL_TEMPLATE.format(
            lon1=lon1, lat1=lat1,
            lon2=lon2, lat2=lat2
        )
        response = requests.get(url, timeout=OSRM_TIMEOUT_S).json()
        return round(response["routes"][0]["distance"] / 1000, 2)
    except Exception:
        return None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def process_csv(df, progress_callback=None):
    """
    Zpracuje celý DataFrame – pro každý řádek spočítá vzdálenost.
    progress_callback(current, total) – volitelná funkce pro progress bar.
    """
    results_km     = []
    results_status = []
    total          = len(df)

    for i, row in df.iterrows():
        z_lat, z_lon   = geocode(row[CSV_COL_FROM_ZIP], row[CSV_COL_FROM_COUNTRY])
        do_lat, do_lon = geocode(row[CSV_COL_TO_ZIP],   row[CSV_COL_TO_COUNTRY])

        if z_lat is not None and do_lat is not None:
            dist = distance_osrm(z_lat, z_lon, do_lat, do_lon)
            if dist is None:
                dist = haversine(z_lat, z_lon, do_lat, do_lon)
            results_km.append(dist)
            results_status.append(CSV_STATUS_OK)
        else:
            results_km.append(None)
            results_status.append(CSV_STATUS_ERROR)

        if progress_callback:
            progress_callback(i + 1, total)

        time.sleep(NOMINATIM_DELAY_S)

    result_df = df.copy()
    result_df[CSV_COL_DISTANCE_KM] = results_km
    result_df[CSV_COL_STATUS]      = results_status
    return result_df
