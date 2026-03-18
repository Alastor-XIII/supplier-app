import streamlit as st
import pandas as pd
import os

# 🔥 DB file (ต้องอยู่บนสุด)
DB_FILE = "contractors_db.csv"

st.set_page_config(page_title="Supplier Database", layout="wide")

st.title("👷 Supplier Management System")

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


def save_data(df):
    df.to_csv(DB_FILE, index=False)


# --- SESSION ---
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- ADD FORM ---
st.header("➕ Add New Supplier")

with st.form("add_form"):
    name = st.text_input("Company Name")
    type_ = st.text_input("Category")
    phone = st.text_input("Phone")
    contact = st.text_input("Contact Person")
    email = st.text_input("Email")
    location = st.text_input("Location")
    note = st.text_area("Note")

    submit = st.form_submit_button("Save")

    if submit:
        if name and phone:
            new_row = {
                "name": name,
                "type": type_,
                "phone": phone,
                "contact_person": contact,
                "email": email,
                "location": location,
                "note": note
            }

            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True
            )

            save_data(st.session_state.df)
            st.success("Saved!")
        else:
            st.error("Please fill Name and Phone")


# --- DISPLAY ---
st.header("📋 Supplier List")

if not st.session_state.df.empty:
    st.dataframe(st.session_state.df, use_container_width=True)
else:
    st.info("No data yet")
