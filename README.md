# 🚚 BigBag Shipping – End-to-End Python POC

An end-to-end **shipping management proof of concept (POC)** built using **FastAPI**, **Streamlit**, **MySQL**, and **Docker**.

This project demonstrates how a global shipping company can allow customers to book and ship parcels across countries while enforcing **country-specific shipping rules** such as weight limits, size limits, customs duty, and banned items.

---

## 📌 Problem Statement

**Big Bag** is an international shipping company that allows customers to ship parcels between countries.

Each destination country has specific rules:

* Maximum allowed weight
* Maximum allowed size
* Customs duty percentage
* List of banned items

Customers should be able to:

* Create an account
* Create a shipping order
* Get shipping cost based on destination rules
* Place an order only if all rules are satisfied

---

## 🧠 Solution Overview

The application follows a clean **frontend–backend–database** architecture:

```
Streamlit (Frontend)
        |
        |  REST API (JSON)
        v
FastAPI (Backend)
        |
        |  ORM (SQLAlchemy)
        v
MySQL (Database)
```

All components can be run **locally** or **fully containerized using Docker Compose**.

---

## 🛠️ Tech Stack

| Layer     | Technology              |
| --------- | ----------------------- |
| Frontend  | Streamlit               |
| Backend   | FastAPI                 |
| Database  | MySQL                   |
| ORM       | SQLAlchemy              |
| Container | Docker & Docker Compose |
| Language  | Python 3                |

---

## 📂 Project Structure

```
Shipping/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   ├── countries.py
│   │   │   └── orders.py
│   │   └── services/
│   │       └── order_service.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── home.py
│   ├── pages/
│   │   ├── signup.py
│   │   └── create_order.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

## 🗄️ Database Design

### Users

* `id`, `name`, `email`, `password`

### Countries

* `id`, `name`, `max_weight`, `max_size`, `customs_duty_percent`

### Banned Items

* `id`, `item_name`, `country_id`

### Orders

* `id`, `user_id`, `country_id`, `item_name`
* `weight`, `size`, `shipping_cost`, `status`

---

## 🔄 Order Processing Flow

1. User creates an account
2. User enters parcel details and destination country
3. Backend validates:

   * Weight ≤ max allowed weight
   * Size ≤ max allowed size
   * Item is not banned
4. Shipping cost calculation:

   ```
   base_cost = weight × base_rate
   customs = base_cost × customs_percentage
   total_cost = base_cost + customs
   ```
5. Order is saved only if all validations pass

---

# ▶️ How to Run the Project

## ✅ Option 1: Run Using Docker (Recommended)

### Prerequisites

* Docker Desktop installed and running
* Docker Compose enabled

### Steps

From the **project root**:

```bash
docker-compose up --build
```

### Access URLs

* **Backend API (Swagger UI):**
  [http://localhost:8000/docs](http://localhost:8000/docs)

* **Frontend (Streamlit UI):**
  [http://localhost:8501](http://localhost:8501)

✅ This starts **MySQL, FastAPI, and Streamlit** together.

---

## ✅ Option 2: Run Locally (Without Docker)

### 1️⃣ Run MySQL

* Start MySQL locally
* Create database:

```sql
CREATE DATABASE bigbag;
```

---

### 2️⃣ Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bigbag
DB_USER=root
DB_PASSWORD=root
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

### 3️⃣ Frontend Setup (Streamlit)

```bash
cd frontend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run home.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 🧪 Testing the Application

1. Open Swagger UI
   👉 `http://localhost:8000/docs`
2. Create a **Country**
3. Open Streamlit UI
   👉 Register a **User**
4. Create an **Order**
5. Try invalid cases:

   * Overweight parcel
   * Banned item

---

## 🔐 Environment Variables

Environment variables are stored in `.env` files and **not committed to Git**:

```env
DB_HOST=db
DB_PORT=3306
DB_NAME=bigbag
DB_USER=root
DB_PASSWORD=root
```

---

## 🎯 Key Highlights

* Clean separation of concerns
* Backend-driven business validation
* Dynamic shipping cost calculation
* Dockerized for easy deployment
* Interview-ready architecture

---

## 🧠 Interview Summary

> “I implemented a rule-based shipping system using FastAPI and Streamlit.
> Country-specific rules are enforced at the backend, pricing is calculated dynamically, and the application is containerized using Docker Compose.”

---

## 🚀 Future Enhancements

* JWT authentication
* Password hashing
* Admin UI for country rule management
* Unit & integration tests
* Cloud deployment (AWS / Azure / Render)

---

## 👤 Author

**Vinil Wani**
Python Developer
