import streamlit as st
import pandas as pd
import os

# --- 1. SETTINGS & FILE PATH ---


# --- 2. DATA FUNCTIONS ---
def load_data():
    cols = ["name", "type", "phone", "contact_person", "email", "location", "note"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            for col in cols:
                if col not in df.columns: df[col] = ""
            return df
        except:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)


def save_data(df):
    df.to_csv(DB_FILE, index=False)


# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = load_data()


# --- 3. EDIT DIALOG ---
@st.dialog("Edit Supplier Details")
def edit_dialog(index, row_data):
    st.write(f"Editing: **{row_data['name']}**")
    with st.form("edit_form"):
        e_name = st.text_input("Company Name", value=row_data['name'])
        e_type = st.text_input("Category", value=row_data['type'])
        e_phone = st.text_input("Phone Number", value=row_data['phone'])
        e_contact = st.text_input("Contact Person", value=row_data['contact_person'])
        e_email = st.text_input("Email", value=row_data['email'])
        e_loc = st.text_input("Location", value=row_data['location'])
        e_note = st.text_area("Notes", value=row_data['note'])

        if st.form_submit_button("Update", type="primary"):
            st.session_state.df.at[index, 'name'] = e_name
            st.session_state.df.at[index, 'type'] = e_type
            st.session_state.df.at[index, 'phone'] = e_phone
            st.session_state.df.at[index, 'contact_person'] = e_contact
            st.session_state.df.at[index, 'email'] = e_email
            st.session_state.df.at[index, 'location'] = e_loc
            st.session_state.df.at[index, 'note'] = e_note
            save_data(st.session_state.df)
            st.success("Record Updated!")
            st.rerun()


# --- 4. MAIN INTERFACE ---
st.set_page_config(page_title="Supplier Database", layout="wide")
st.title("👷 Supplier Management System")

tab1, tab2 = st.tabs(["🔍 Search & Filter", "➕ Add New Supplier"])

# --- TAB 1: SEARCH ---
with tab1:
    if not st.session_state.df.empty:
        categories = ["All"] + sorted(st.session_state.df["type"].unique().tolist())
        selected = st.pills("Filter by Category:", categories, default="All")
        st.divider()

        display_df = st.session_state.df if selected == "All" else st.session_state.df[
            st.session_state.df["type"] == selected]

        if not display_df.empty:
            for idx, row in display_df.iterrows():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.subheader(row['name'])
                        st.markdown(f"**Category:** `{row['type']}`")
                        st.markdown(f"📍 **Location:** {row['location']}")
                    with c2:
                        st.write(f"👤 **Contact:** {row['contact_person']}")
                        st.write(f"📞 **Phone:** {row['phone']}")
                        st.write(f"📧 **Email:** {row['email']}")
                    with c3:
                        if st.button("📝 Edit", key=f"edit_{idx}", use_container_width=True):
                            edit_dialog(idx, row)
                        if st.button("🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                            st.session_state.df = st.session_state.df.drop(idx).reset_index(drop=True)
                            save_data(st.session_state.df)
                            st.rerun()
                    if row['note']: st.info(f"Notes: {row['note']}")
        else:
            st.info("No records found.")
    else:
        st.info("No data available. Please add a supplier.")

# --- TAB 2: ADD NEW ---
with tab2:
    st.header("Register New Supplier")
    existing_types = sorted(st.session_state.df["type"].unique().tolist()) if not st.session_state.df.empty else []

    with st.form("add_supplier_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Company Name *")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
        with col2:
            # Re-added the logic for category selection
            type_choice = st.selectbox("Select Category", ["(Add New Category)"] + existing_types)

            # This field only shows up in the form logic when submitted or handled
            new_type_input = st.text_input("Or type new category name here...")

            phone = st.text_input("Phone Number *")
            location = st.text_input("Address/Location")

        note = st.text_area("Additional Information")

        submit = st.form_submit_button("Save to Database", type="primary")

        if submit:
            # Logic: If user typed in the box, use that. Otherwise use selectbox.
            final_type = new_type_input.strip() if new_type_input.strip() != "" else type_choice

            if name and phone and (final_type and final_type != "(Add New Category)"):
                new_entry = {
                    "name": name, "type": final_type, "phone": phone,
                    "contact_person": contact_person, "email": email,
                    "location": location, "note": note
                }
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
                save_data(st.session_state.df)
                st.success(f"Successfully added {name}!")
                st.rerun()
            else:
                st.error("Please provide Name, Phone, and Category.")