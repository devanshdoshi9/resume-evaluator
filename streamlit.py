import requests

import streamlit as st

st.title("Resume Evaluator")

skills = st.text_input("Skill list (comma separated):", placeholder="Java, Python, SQL...")

uploaded_file = st.file_uploader("Choose a file", type=[".pdf"])

if st.button("Evaluate") and uploaded_file:
    response = requests.post("http://localhost:8000/resume/upload",
                             params={"skills_to_match": skills, "filename": uploaded_file.name},
                             files={"file": uploaded_file.getvalue()})

    st.json(response.json(), expanded=True)
