import streamlit as st
import config as cfg

class Menu:
    def __init__(self):
        st.set_page_config(
            page_title="Useful office apps",
            page_icon="🚛🚂⚓",
            layout="wide"
        )

    def zobrazit_menu(self):
        st.title("Vítej v aplikaci! 👋")
        st.subheader("Vytvořil: Marchi8ni@gmail.com")
        st.sidebar.header("Menu")
        name = st.sidebar.text_input("Jaké je tvoje jméno?")
        sekce = st.sidebar.radio("Vyber sekci:", ["Domů", "Výpočet vzdálenosti mezi PSČ", "Open orders report"])
        return name, sekce

    @staticmethod
    def centered_column(ratio: int = 2):
        """Vrátí prostřední sloupec pro centrovaný obsah."""
        left, middle, right = st.columns([1, ratio, 1])
        return middle

    def styly(self):
        st.markdown(
            """
            <style>
            .big-red {
                color: red;
                font-size: 40px;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
# --- Použití ---
menu = Menu()
menu.styly()  # načte styly

# vykreslení textu s CSS třídou
st.markdown("<p class='big-red'>Tento text je červený a velký</p>", unsafe_allow_html=True)