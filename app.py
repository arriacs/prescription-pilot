import streamlit as st

# Page configuration
st.set_page_config(
    page_title = "Prescription Pilot",
    page_icon = "💊",
    layout="wide"
)

# Website title
st.title("Prescription Pilot")

# Description
st.write("An app for easy access and changes to all you presciptions!")

# Sidebar
st.sidebar.title("Navigation")

# User Input
drug_name = st.text_input("Search for a drug:")

# Search button
if st.button("Search"):
    if drug_name:
        st.write(f"Searching for: {drug_name}")
    else:
        st.warning("Please enter a drug name")