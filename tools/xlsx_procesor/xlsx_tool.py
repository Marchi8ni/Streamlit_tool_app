# =============================================================================
# xlsx_logic.py – Logika zpracování Excel souboru (bez Streamlit)
# =============================================================================

import pandas as pd
from io import BytesIO
from datetime import datetime
from config import XLSX_COLUMN_SEQUENCE


def load_sheets(file):
    """
    Načte všechny listy z Excel souboru.
    Vrátí slovník {název listu: DataFrame}
    """
    return pd.read_excel(file, sheet_name=None)


def find_pivot_header_row(ws):
    """
    Najde řádek kde začíná pivot tabulka
    (hledá buňku s textem 'Popisky řádků').
    Vrátí index řádku.
    """
    mask = ws.eq("Popisky řádků").any(axis=1)
    matching = ws[mask].index
    if len(matching) == 0:
        raise ValueError("Sloupec 'Popisky řádků' nebyl nalezen v listu.")
    return matching[0]


def process_sheet(ws):
    """
    Zpracuje list pivot tabulky:
    - najde záhlaví
    - přeuspořádá sloupce dle config.py
    - odstraní prázdné řádky

    Vrátí dvojici (result_df, missing_cols)
    """
    header_row = find_pivot_header_row(ws)

    ws.columns = ws.iloc[header_row]
    ws = ws.iloc[header_row + 1:]
    ws = ws.reset_index(drop=True)

    ws = ws.dropna(how="all")

    existing_cols = [c for c in XLSX_COLUMN_SEQUENCE if c in ws.columns]
    missing_cols  = [c for c in XLSX_COLUMN_SEQUENCE if c not in ws.columns]

    ws = ws[existing_cols]

    return ws, missing_cols


def export_to_excel(df):
    """
    Exportuje DataFrame do Excel souboru v paměti.
    Vrátí BytesIO objekt připravený ke stažení.
    """
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output


def get_output_filename():
    """Vrátí název výstupního souboru s dnešním datem."""
    return f"report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"