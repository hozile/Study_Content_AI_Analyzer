# difficulty_page.py
import streamlit as st
from study_content_ai_analyzer import aim

def display_difficulty_page():
    st.title("⛏Difficulty Selection")
    st.write("This is the difficulty selection page.")

    difficulty = st.radio("Choose a Difficulty", ["Easy", "Medium", "Hard"])
    st.session_state.difficulty_selected = difficulty

    if st.button("Generate Questions with Selected Difficulty"):
        file_content = st.session_state.get("file_content")
        st.info("**Please be patient... Your AI-Generated Questions are on the way!**")
        questions_list = aim.content_generator(file_content,difficulty)
        st.session_state.question_list_generated = questions_list

        st.success("AI has generated your questions successfully!✨")
        st.session_state.question_generated = "Third Generated"

    if st.session_state.question_generated == "Third Generated":
        if st.button("Start Answer"):
            st.session_state["submitted"] = False
            st.session_state.page = "app"  # Set page to app
