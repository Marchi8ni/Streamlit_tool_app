# =============================================================================
# ui/xlsx_ui.py – Streamlit UI pro XLSX procesor
# =============================================================================

import streamlit as st
from tools.xlsx_procesor.xlsx_tool import load_sheets, process_sheet, export_to_excel, get_output_filename


def render_xlsx_tool():

    st.markdown("### 📊 XLSX procesor")
    st.caption("Nahraj Excel soubor s pivot tabulkou – aplikace přeuspořádá sloupce a připraví výstup ke stažení.")
    st.divider()

    # --- KROK 1: Upload ---
    st.markdown("#### Krok 1 – Nahrát Excel soubor")
    uploaded_file = st.file_uploader(
        label="Vyber Excel soubor",
        type=["xlsx"],
    )

    if uploaded_file is not None:

        try:
            sheets = load_sheets(uploaded_file)
        except Exception as e:
            st.error(f"Nepodařilo se načíst soubor: {e}")
            st.stop()

        st.success(f"✅ Soubor nahrán – nalezeno {len(sheets)} listů")

        # --- KROK 2: Výběr listu ---
        st.markdown("#### Krok 2 – Vyber list s pivot tabulkou")
        sheet_name = st.selectbox("Vyber list:", list(sheets.keys()))

        st.divider()

        # --- KROK 3: Zpracování ---
        st.markdown("#### Krok 3 – Zpracovat soubor")

        if st.button("⚙️ Zpracovat soubor", type="primary"):

            try:
                ws = sheets[sheet_name]
                result_df, missing_cols = process_sheet(ws)

                if missing_cols:
                    st.warning(f"⚠️ Tyto sloupce nebyly nalezeny: {missing_cols}")

                st.session_state["xlsx_result"] = result_df
                st.success("✅ Hotovo!")

            except ValueError as e:
                st.error(f"Chyba při zpracování: {e}")
                st.stop()

    # --- KROK 4: Výsledky a stažení ---
    if "xlsx_result" in st.session_state:

        st.divider()
        st.markdown("#### Krok 4 – Výsledky")

        result_df = st.session_state["xlsx_result"]

        st.dataframe(result_df, use_container_width=True, height=320)

        output   = export_to_excel(result_df)
        filename = get_output_filename()

        st.download_button(
            label="📥 Stáhnout výsledný Excel",
            data=output,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )