import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
from fpdf import FPDF
import hashlib
import pytz

# === Secure Password Protection ===
def get_hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

correct_password_hash = get_hashed_password("MayFly2025!")

def check_password():
    def password_entered():
        entered_password_hash = get_hashed_password(st.session_state["password"])
        if entered_password_hash == correct_password_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect. Try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# === Domestic route filter ===
DOMESTIC_ROUTES = ["LHRABZ", "LHRINV", "LHRGLA", "LHREDI", "LHRBHD", "LHRNCL", "LHRJER", "LHRMAN", "LHRBFS", "LHRDUB"]
# === Terminal 3 flight numbers ===
T3_FLIGHTS = [
    "BA159","BA227","BA247","BA253","BA289","BA336","BA340","BA350","BA366","BA368","BA370",
    "BA372","BA374","BA376","BA378","BA380","BA382","BA386","BA408","BA410","BA416","BA418",
    "BA422","BA490","BA492","BA498","BA532","BA608","BA616","BA618","BA690","BA696","BA700",
    "BA702","BA704","BA706","BA760","BA762","BA764","BA766","BA770","BA790","BA792","BA802",
    "BA806","BA848","BA852","BA854","BA856","BA858","BA860","BA862","BA864","BA866","BA868",
    "BA870","BA872","BA874","BA882","BA884","BA886","BA890","BA892","BA896","BA918","BA920"
]

# === Main App ===
BA_BLUE = (0, 32, 91)
LIGHT_RED = (255, 204, 204)
AMBER = (255, 229, 153)

class BA_PDF(FPDF):
    def __init__(self, date_str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_str = date_str

    def header(self):
        self.set_fill_color(*BA_BLUE)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'MayFly {self.date_str} - British Airways', ln=True, align='C', fill=True)
        self.ln(5)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(0)
        self.multi_cell(0, 5,
            "Please note, Conformance times below are for landside only. "
            "If you're working in connections, add 5 minutes to the conformance time. "
            "E.g. landside conformance is 10:00, connections conformance is 10:05.",
            align='C'
        )
        self.ln(3)

    def footer(self):
