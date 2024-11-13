import streamlit as st
import pandas as pd
from study_content_ai_analyzer import aim, db

def display_upload_page():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f9f9f9;
        }
        .header {
            font-size: 30px;
            color: #4a4a4a;
            font-weight: bold;
        }
        .subheader {
            font-size: 18px;
            color: #6e6e6e;
        }
        .file-section {
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            background-color: #ffffff;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        div.stButton > button:first-child {
            background-color: #0099ff;
            color: #ffffff;
        }
        div.stButton > button:hover {
            background-color: #007acc;
            color: #ffffff;
            border: 2px solid #000000;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state if not already set
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'  # Default page is 'upload'
    if 'question_generated' not in st.session_state:
        st.session_state.question_generated = False  # Track if questions have been generated

    # Display page content based on the current session state
    if st.session_state.page == 'upload':
        # Title and Description
        st.markdown("<div class='header'>📂 Study Content AI Analyzer</div>", unsafe_allow_html=True)
        st.markdown("<div class='subheader'>Easily upload files, choose from your uploaded files, and generate AI content.</div>", unsafe_allow_html=True)

        # File Upload Section
        st.subheader("Step 1: Upload Your Files")
        uploaded_files = st.file_uploader("Choose files to upload", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Uploaded File's Details")

        for file in uploaded_files:
            file_actual_size = round(file.size / 1024, 2)  # Convert file size to KB

            # Check if file size is within the limit
            if file_actual_size > 15000:
                # Display a warning for files exceeding the size limit
                st.error(f"The file exceeds 15000 KB and is not supported")
            else:
                st.success("Files uploaded successfully!")
                file_details = [{"Filename": file.name, "Type": file.type, "Size (KB)": file_actual_size}]
                df_files = pd.DataFrame(file_details)
                st.table(df_files)  # Display details for files within size limit

                # Step 2: File Selection
                st.subheader("Step 2: Select a File to Generate Questions With AI")
                selected_file = st.selectbox(
                    "Choose a file to generate questions",
                    options=uploaded_files,
                    format_func=lambda x: x.name,
                    key=f"selectbox_{file.name}"  # Use a unique key for each selectbox
                )

                if selected_file:
                    file_content = selected_file.read().decode("utf-8", errors="ignore")
                    st.write(f"**Selected File:** {selected_file.name}")

                    # Button to generate questions
                    if st.button("Confirm to generate questions with AI Model", key=f"confirm_button_{file.name}"):
                        st.session_state["filename_selected"] = selected_file.name
                        st.session_state.question_generated = "Select Difficulty"  # Update flag to enable Difficulty button
                        st.session_state.file_content =  file_content # Update flag to enable Difficulty button

                    if st.session_state.question_generated == "Select Difficulty":
                        st.subheader("**Select Difficulty**")
                        if st.button("Select Difficulty", key=f"difficulty_button_{file.name}"):
                            st.session_state.page = 'difficulty'  # Navigate to difficulty page
