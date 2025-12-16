import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("📦 Create Shipping Order")

# Load countries
countries_res = requests.get(f"{API_BASE}/countries")
countries = countries_res.json()

country_map = {c["name"]: c["id"] for c in countries}

user_id = st.number_input("User ID", min_value=1, step=1)
item_name = st.text_input("Item Name")
weight = st.number_input("Weight (kg)", min_value=0.1)
size = st.number_input("Size (cm)", min_value=0.1)
country_name = st.selectbox("Destination Country", list(country_map.keys()))

if st.button("Calculate & Place Order"):
    payload = {
        "user_id": user_id,
        "country_id": country_map[country_name],
        "item_name": item_name,
        "weight": weight,
        "size": size
    }

    res = requests.post(f"{API_BASE}/orders", json=payload)

    if res.status_code == 200:
        data = res.json()
        st.success(f"Order placed! Shipping cost: ₹{data['shipping_cost']}")
    else:
        st.error(res.json().get("detail", "Order failed"))
