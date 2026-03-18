import streamlit as st
import pandas as pd
import os

# 🔥 ต้องอยู่ตรงนี้
DB_FILE = "contractors_db.csv"


# --- DATA FUNCTIONS ---
def load_data():
    cols = ["name", "type", "phone", "contact_person", "email", "location", "note"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            for col in cols:
                if col not in df.columns:
                    df[col] = ""
            return df
        except:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)


# 🔥 เรียกใช้ตรงนี้ได้
if 'df' not in st.session_state:
    st.session_state.df = load_data()
