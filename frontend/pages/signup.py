import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("👤 Create Account")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    payload = {
        "name": name,
        "email": email,
        "password": password
    }

    res = requests.post(f"{API_BASE}/users", json=payload)

    if res.status_code == 200:
        st.success("Account created successfully")
    else:
        st.error(res.json().get("detail", "Error occurred"))
