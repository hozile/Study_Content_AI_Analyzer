# main.py
import streamlit as st
from upload_page import display_upload_page
from difficulty_page import display_difficulty_page
from app_page import display_app_page

# Initialize session state for page navigation if not set
if 'page' not in st.session_state:
    st.session_state.page = 'upload'

# Page Navigation Logic
if st.session_state.page == 'upload':
    display_upload_page()
elif st.session_state.page == 'difficulty':
    display_difficulty_page()
elif st.session_state.page == 'app':
    display_app_page() 
