# 🚚 Shipping POC – Big Bag Shipping Company

A proof-of-concept system for an international shipping company (**Big Bag**) that allows customers to book and ship parcels across countries while enforcing destination-based shipping rules.

---

## 📌 Project Overview
This POC demonstrates the essential workflow of a global shipping platform, including customer onboarding, country rule management, automatic parcel validation, and order processing with cost calculations.

---

## ✨ Key Features

### 🧑‍💻 Customer Features
- Create an account and log in
- Get instant shipping cost estimates
- Create, view, and manage shipping orders
- Automatic validation for banned items, weight, and size

### 🛠️ Admin Features
- Add and manage countries with ISO codes
- Set shipping rules (max weight, max size, custom duty %)
- Maintain banned-item lists per country

---

## 🌍 Country Rule Engine
Each country includes:
- Maximum parcel weight  
- Maximum parcel size  
- Custom duty percentage  
- List of banned items  

These rules ensure accurate validation and safe shipment handling.

---

## 🧠 Order Processing Flow
1. Customer submits parcel details  
2. System validates size, weight, and restricted items  
3. Shipping cost is calculated using country-specific rules  
4. Order becomes **Pending**, **Confirmed**, or **Rejected**

---

## 🏗️ Tech Stack
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Database:** MySQL  
- **ORM:** SQLAlchemy  
- **Validation & Security:** Pydantic, password hashing  

---

## 📂 Project Structure (High-Level)
```
shipping-poc/
├── backend/      # Backend services (FastAPI)
├── frontend/     # User interface (Streamlit)
└── README.md
```

---

## 🚀 Getting Started (Summary)
1. Install dependencies for backend & frontend  
2. Set up MySQL database  
3. Start FastAPI backend  
4. Run Streamlit frontend  

---

## 📜 Status
This is a **proof-of-concept project**, intended for demonstration and learning purposes.
