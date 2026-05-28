# =====================================================================
# ui/layout.py – Sdílené UI komponenty (sidebar, načtení CSS)
# =====================================================================

import streamlit as st
from pathlib import Path


def load_css():
    """Načte custom CSS ze souboru a aplikuje ho na celou aplikaci."""
    css_path = Path(__file__).parent / "styles" / "main.css"
    with open("Ui/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_sidebar(tools: list) -> str:
    """
    Vykreslí sidebar s navigací.

    Args:
        tools: seznam názvů nástrojů např. ["📍 PSČ kalkulačka"]

    Returns:
        název vybraného nástroje
    """
    with st.sidebar:
        st.markdown( "<h2 style='color:white; margin-bottom:0;'>🛠️ Python Toolbox</h2>",
        unsafe_allow_html=True)
        st.caption("v1.0.0")
        st.divider()
        st.markdown("**Nástroje**")
        selected = st.radio(
            label="Nástroj",
            options=tools,
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown(
            "<span style='opacity:0.45; font-size:13px;'>📊 XLSX procesor</span><br>"
            "<span style='opacity:0.45; font-size:13px;'>➕ Nástroj 3</span>",
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown(
            "<span style='font-size:13px;'>⚙️ Nastavení</span>",
            unsafe_allow_html=True,
        )

    return selected