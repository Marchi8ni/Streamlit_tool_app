# =============================================================================
# app.py – Hlavní soubor aplikace Python Toolbox
# =============================================================================
# Spuštění: streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
from config import (
    APP_NAME, APP_ICON, APP_VERSION,
    PRIMARY_COLOR, ACCENT_COLOR,
    MAX_FILE_SIZE_MB, CSV_REQUIRED_COLUMNS,
)
from tools.distance_calculator.distance_calculator_logic import (process_csv)
from Ui.layout import load_css, render_sidebar
from Ui.xlsx_ui import render_xlsx_tool

# =============================================================================
# Konfigurace stránky
# =============================================================================

st.set_page_config(
    page_title="Python Toolbox",
    page_icon="🛠️",
    layout="wide",
)

# =============================================================================
# Načtení CSS
# =============================================================================

load_css()

# =============================================================================
# Sidebar
# =============================================================================

selected = render_sidebar(["📍 PSČ kalkulačka", "📊 XLSX procesor"])

# =============================================================================
# PSČ kalkulačka
# =============================================================================

if selected == "📍 PSČ kalkulačka":

    st.markdown("### 📍 Výpočet vzdálenosti mezi PSČ")
    st.caption("Nahraj CSV se sloupci z_PSČ, z_Země, do_PSČ, do_Země")
    st.divider()

    # --- KROK 1: Upload ---
    st.markdown("#### Krok 1 – Nahrát CSV soubor")
    uploaded_file = st.file_uploader(
        label="Vyber CSV soubor",
        type=["csv"],
        help=f"Povinné sloupce: {', '.join(CSV_REQUIRED_COLUMNS)}",
    )

    if uploaded_file is not None:

        # Kontrola velikosti
        size_mb = uploaded_file.size / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            st.error(f"Soubor je příliš velký ({size_mb:.1f} MB). Maximum je {MAX_FILE_SIZE_MB} MB.")
            st.stop()

        # Načtení CSV
        try:
            df = pd.read_csv(uploaded_file, sep=None, engine="python")
        except Exception as e:
            st.error(f"Nepodařilo se načíst CSV: {e}")
            st.stop()

        # Validace sloupců
        missing = [col for col in CSV_REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            st.error(f"Chybějící sloupce: {', '.join(missing)}")
            st.stop()

        # Potvrzení
        col1, col2, col3 = st.columns(3)
        col1.metric("Řádků", f"{len(df):,}")
        col2.metric("Sloupců", len(df.columns))
        col3.metric("Velikost", f"{size_mb:.1f} MB")

        st.success(f"✅ Soubor nahrán")

        with st.expander("Náhled dat"):
            st.dataframe(df.head(5), use_container_width=True)

        st.divider()

        # --- KROK 2: Výpočet ---
        st.markdown("#### Krok 2 – Spustit výpočet")
        st.info(f"Připraveno **{len(df):,} dvojic** PSČ.")

        if st.button("🚀 Spustit výpočet", type="primary"):

            progress_bar = st.progress(0, text="Spouštím výpočet…")

            def update_progress(current, total):
                pct = current / total
                progress_bar.progress(pct, text=f"Zpracováno {current} / {total}…")

            result_df = process_csv(df, progress_callback=update_progress)

            progress_bar.progress(1.0, text="✅ Hotovo!")
            st.session_state["result_df"] = result_df

    # --- KROK 3: Výsledky ---
    if "result_df" in st.session_state:

        st.divider()
        st.markdown("#### Krok 3 – Výsledky")

        result_df = st.session_state["result_df"]

        ok_count  = (result_df["stav"] == "ok").sum()
        err_count = (result_df["stav"] == "chyba").sum()
        avg_km    = result_df["vzdalenost_km"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Úspěšně vypočteno", f"{ok_count:,}")
        col2.metric("Chybné záznamy",    f"{err_count:,}")
        col3.metric("Průměrná vzdálenost", f"{avg_km:.1f} km" if pd.notna(avg_km) else "—")

        st.dataframe(result_df, use_container_width=True, height=320)

        st.divider()
        csv_bytes = result_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ Stáhnout výsledky CSV",
            data=csv_bytes,
            file_name="vysledky.csv",
            mime="text/csv",
            type="primary",
        )
if selected == "📊 XLSX procesor":
    render_xlsx_tool()