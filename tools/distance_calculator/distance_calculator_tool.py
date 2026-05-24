import streamlit as st
import pandas as pd
import requests
import time
import math

st.title("Výpočet vzdálenosti (PSČ → PSČ)")

uploaded_file = st.file_uploader("Nahraj CSV", type=["csv"])

# ---------- CACHE ----------
geo_cache = {}

# ---------- FUNKCE ----------

def normalize_postcode(psc):
    return str(psc).zfill(5)


# ✅ GEOCODING (finální verze)
def geocode(postal_code, country):
    try:
        postal_code = normalize_postcode(postal_code)
        key = f"{postal_code}_{country}"

        if key in geo_cache:
            return geo_cache[key]

        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{postal_code}, {country}",  # ✅ hlavní změna
            "countrycodes": country.lower(),  # ✅ filtr na zemi
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "streamlit-distance-app"
        }

        response = requests.get(url, params=params, headers=headers).json()

        if len(response) == 0:
            geo_cache[key] = (None, None)
            return None, None

        lat = float(response[0]["lat"])
        lon = float(response[0]["lon"])

        geo_cache[key] = (lat, lon)

        return lat, lon

    except Exception as e:
        st.error(f"Geocode error: {e}")
        return None, None


# ✅ OSRM distance (silniční)
def distance_osrm(lat1, lon1, lat2, lon2):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        response = requests.get(url).json()

        return response['routes'][0]['distance'] / 1000  # km

    except:
        return None


# ✅ Haversine (fallback)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


# ---------- HLAVNÍ LOGIKA ----------

if uploaded_file:

    st.success("Soubor nahrán ✅")

    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
        st.success("CSV načteno ✅")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Chyba při načítání CSV: {e}")
        st.stop()


    if st.button("Spočítat vzdálenosti"):

        results = []

        for i, row in df.iterrows():

            st.write(f"➡️ Řádek {i+1}/{len(df)}")

            # ✅ geocode
            z_lat, z_lon = geocode(row["z_psc"], row["z_zeme"])
            do_lat, do_lon = geocode(row["do_psc"], row["do_zeme"])

            st.write(f"Z: {row['z_psc']} → {z_lat}, {z_lon}")
            st.write(f"DO: {row['do_psc']} → {do_lat}, {do_lon}")

            # ✅ výpočet vzdálenosti
            if z_lat is not None and do_lat is not None:

                dist = distance_osrm(z_lat, z_lon, do_lat, do_lon)

                # fallback
                if dist is None:
                    st.write("⚠️ fallback → vzdušná vzdálenost")
                    dist = haversine(z_lat, z_lon, do_lat, do_lon)

            else:
                dist = None

            results.append(dist)

            time.sleep(1)  # OSM limit

        df["distance_km"] = results

        st.success("Hotovo ✅")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Stáhnout CSV",
            csv,
            "vysledek.csv",
            "text/csv"
        )
