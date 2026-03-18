import streamlit as st
import pandas as pd
import os

# 🔥 DB file
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

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None


# --- ADD / EDIT FORM ---
st.header("➕ Add / Edit Supplier")

with st.form("form"):
    edit_mode = st.session_state.edit_index is not None

    if edit_mode:
        row = st.session_state.df.loc[st.session_state.edit_index]
    else:
        row = {}

    name = st.text_input("Company Name", value=row.get("name", ""))
    type_ = st.text_input("Category", value=row.get("type", ""))
    phone = st.text_input("Phone", value=row.get("phone", ""))
    contact = st.text_input("Contact Person", value=row.get("contact_person", ""))
    email = st.text_input("Email", value=row.get("email", ""))
    location = st.text_input("Location", value=row.get("location", ""))
    note = st.text_area("Note", value=row.get("note", ""))

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Save")
    with col2:
        cancel = st.form_submit_button("Cancel")

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

            if edit_mode:
                st.session_state.df.loc[st.session_state.edit_index] = new_row
                st.success("Updated!")
            else:
                st.session_state.df = pd.concat(
                    [st.session_state.df, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                st.success("Saved!")

            save_data(st.session_state.df)
            st.session_state.edit_index = None
            st.rerun()
        else:
            st.error("Please fill Name and Phone")

    if cancel:
        st.session_state.edit_index = None
        st.rerun()


# --- DISPLAY ---
st.header("📋 Supplier List")

if not st.session_state.df.empty:
    for i, row in st.session_state.df.iterrows():
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            st.write(f"**{row['name']}** | {row['type']} | {row['phone']}")

        with col2:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.rerun()

        with col3:
            if st.button("🗑️ Delete", key=f"del_{i}"):
                st.session_state.df = st.session_state.df.drop(i).reset_index(drop=True)
                save_data(st.session_state.df)
                st.rerun()
else:
    st.info("No data yet")
