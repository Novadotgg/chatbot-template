import streamlit as st
from transformers import pipeline

st.title("PG-AGI ML/AI Assignment")

# Initialize candidate info
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {
        "Full Name": "",
        "Email": "",
        "Phone Number": "",
        "Years of Experience": "",
        "Desired Position": "",
        "Current Location": "",
        "Tech Stack": []
    }

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Welcome to the AI interview assistant. Let's begin the interview!"}
    ]

questions = [
    "What is your full name?",
    "Please enter your email address.",
    "What is your phone number?",
    "How many years of experience do you have?",
    "Which position are you applying for?",
    "Where are you currently located?",
    "List your tech stack (programming languages, frameworks, databases, tools)."
]

for msg in st.session_state.messages:
    st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")

if st.session_state.question_index < len(questions):
    next_question = questions[st.session_state.question_index]
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != next_question:
        st.session_state.messages.append({"role": "assistant", "content": next_question})
    st.write(f"**Assistant:** {next_question}")

user_input = st.text_input("Your Response:", key="user_input")

if st.button("Submit"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        if st.session_state.question_index < len(st.session_state.candidate_info):
            question_key = list(st.session_state.candidate_info.keys())[st.session_state.question_index]
            
            if question_key == "Tech Stack":
                st.session_state.candidate_info[question_key] = [tech.strip() for tech in user_input.split(",")]
            else:
                st.session_state.candidate_info[question_key] = user_input

        st.session_state.question_index += 1

        if st.session_state.question_index == len(questions):
            tech_stack = ", ".join(st.session_state.candidate_info["Tech Stack"])
            prompt = f"Generate 3-5 technical interview questions for a candidate proficient in {tech_stack}."
            generator = pipeline("text-generation", model="distilgpt2")
            response = generator(prompt, max_length=150, num_return_sequences=1)
            tech_questions = response[0]["generated_text"]
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Great! Based on your tech stack, here are some technical questions:\n{tech_questions}"}
            )
            st.session_state.messages.append({"role": "assistant", "content": "That concludes our interview. Thank you for your time!"})
        st.rerun()
