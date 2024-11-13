import streamlit as st
from study_content_ai_analyzer import db

def display_app_page():
    def display_quiz():
        questions_data = st.session_state.get("question_list_generated")
        
        # Check if questions_data exists
        if not questions_data:
            st.error("No questions available to display. Please generate questions first.")
            return

        print(f"questions_data: {questions_data}")
        answers = {}

        # Apply custom CSS for colors and font size
        st.markdown("""
        <style>
            .question { font-size: 20px; color: #1a73e8; font-weight: bold; margin-bottom: 10px; }
            .option { font-size: 16px; color: #e8eaed; background-color: #303134; padding: 8px; border-radius: 6px; margin-left: 20px; margin-bottom: 10px; }
            .option:hover { background-color: #5f6368; color: #ffffff; }
            .result { font-size: 18px; font-weight: bold; color: #0066cc; }
        </style>
        """, unsafe_allow_html=True)

        st.title("Answer the AI-Generated Questions Below 📝")

        # Display each question with options
        for idx, item in enumerate(questions_data, start=1):  
            question_text = item['question']  # Adjusted key
            options = item['options']         # Adjusted key

            # Display the question number and text using idx as the question number
            st.markdown(f"**Q{idx}: {question_text}**")

            # Display the options as radio buttons
            user_answer = st.radio(
                f"Choose your answer for Question {idx}",
                options,
                key=f"q{idx}",
                index=None
            )

            # Store the user's answer for later evaluation if needed
            answers[f"q{idx}"] = user_answer

        # Button to submit the quiz
        if st.button("Submit Quiz"):
            score = calculate_score(answers, questions_data)
            
            # Store score and answers in session state and mark as submitted
            st.session_state["submitted"] = True
            st.session_state["score"] = score
            st.session_state["answers"] = answers
            st.session_state["questions"] = questions_data
            st.success(f"Quiz submitted! Your score is: {score}/{len(questions_data)}")

    def display_results():
        # Retrieve the score, user answers, and questions from session state
        score = st.session_state.get("score", 0)
        user_answers = st.session_state.get("answers", {})
        questions = st.session_state.get("questions", [])

        # Display final score with color coding based on pass/fail
        pass_threshold = len(questions) // 2
        if score >= pass_threshold:
            # Pass - display score in green
            st.markdown(
                f"<h3 style='color:green;'>Final Result: {score}/{len(questions)}</h3>",
                unsafe_allow_html=True
            )
        else:
            # Fail - display score in red
            st.markdown(
                f"<h3 style='color:red;'>Final Result: {score}/{len(questions)}</h3>",
                unsafe_allow_html=True
            )

        # Loop through each question to display answers and indicate correct/incorrect responses
        for idx, question in enumerate(questions, start=1):
            question_text = question["question"]
            correct_answer = question["answer"]
            user_answer = user_answers.get(f"q{idx}")

            # Display the question
            st.markdown(f"<p class='question'><strong>Q{idx}: {question_text}</strong></p>", unsafe_allow_html=True)

            # Display each option, highlighting the user's answer and indicating correctness
            for option in question["options"]:
                if option == user_answer:
                    if option == correct_answer:
                        color_class = "correct"  # Correct answer color class
                    else:
                        color_class = "incorrect"  # Incorrect answer color class
                    st.markdown(f"<p class='option {color_class}'>{option} (Your Answer)</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='option'>{option}</p>", unsafe_allow_html=True)

            # Show the correct answer if the user was incorrect
            if user_answer != correct_answer:
                st.markdown(f"<p class='correct-answer'>Correct Answer: {correct_answer}</p>", unsafe_allow_html=True)

        # Button to restart the quiz
        if st.button("Restart"):
            st.session_state["question_generated"] = "Second Generated"
            st.session_state["page"] = 'difficulty'

    # CSS styling for improved UI with green/red color coding
    st.markdown("""
    <style>
        .question { font-size: 20px; color: #1a73e8; font-weight: bold; margin-bottom: 10px; }
        .option { font-size: 16px; color: #e8eaed; background-color: #303134; padding: 8px; border-radius: 6px; margin-left: 20px; margin-bottom: 10px; }
        .correct { background-color: #d4edda; color: #155724; font-weight: bold; }  /* Green for correct answers */
        .incorrect { background-color: #f8d7da; color: #721c24; font-weight: bold; }  /* Red for incorrect answers */
        .correct-answer { color: #28a745; font-weight: bold; margin-top: 5px; }
        .result { font-size: 18px; font-weight: bold; color: #0066cc; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

    # Function to calculate the score
    def calculate_score(user_answers, questions):
        print("===========Start Calculating Score ============")
        score = 0
        for idx, question in enumerate(questions):
            correct_answer = question['answer']
            user_answer = user_answers.get(f"q{idx + 1}")  # Account for index mismatch

            # Check if the user's answer matches the correct answer
            if user_answer == correct_answer:
                score += 1

        print(f"Final score: {score}")
        return score

    # Initialize session state for tracking submission
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    # Main app logic: show quiz or results page based on submission status
    if st.session_state["submitted"]:
        display_results()  # Show results page after submission
    else:
        display_quiz()  # Show quiz initially
