import streamlit as st
from wc_ui import apply_theme

# Global page configuration
st.set_page_config(page_title="World Cup Analytics", layout="wide", page_icon="🏆")
apply_theme()

# Define pages
page_experience = st.Page(
    page="pages/1_experience.py", 
    title="The Weight of Experience", 
    icon="1️⃣", 
    default=True # Home page
)

page_hegemony = st.Page(
    page="pages/2_hegemony.py", 
    title="Continental Hegemony", 
    icon="2️⃣"
)

page_first_kick = st.Page(
    page="pages/3_first_kick.py", 
    title="The First Kick Advantage", 
    icon="3️⃣"
)

# Navigation
pg = st.navigation(pages=[page_experience, page_hegemony, page_first_kick])

# Run
pg.run()