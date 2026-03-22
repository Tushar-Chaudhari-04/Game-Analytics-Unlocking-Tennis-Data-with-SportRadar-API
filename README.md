# 🎾 Game Analytics: Tennis Data Pipeline & Dashboard

## 🔥 Key Highlights

* Modular Architecture (**ETL + Streamlit App Separation**)
* End-to-End Data Pipeline (**API → MySQL → Dashboard**)
* Real-world Sports Analytics Use Case
* Secure Credential Handling using **Streamlit Secrets**

---

## 📌 Project Overview

This project builds a complete **data analytics pipeline for tennis data** using API integration, structured storage, and interactive visualization.

It demonstrates how raw sports data can be transformed into meaningful insights using a scalable and modular architecture.

---

## 🎯 Objectives

* Extract tennis data from API
* Transform and clean data using ETL process
* Load structured data into MySQL database
* Perform SQL-based analysis
* Build an interactive dashboard using Streamlit

---

## 🏗️ Architecture

```
API → ETL Pipeline → MySQL Database → Streamlit Dashboard
```

---

## 📂 Project Structure

```
Game-Analytics-Tennis/
│
├── etl/                      # Data extraction + transformation
│   ├── extract/
│   │   ├── api_client.py
│   │   └── extractor.py
│   ├── transform/
│   │   └── transformer.py
│   ├── load/
│   │   ├── db.py
│   │   └── loader.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
│
├── app/                      # Streamlit app
│   ├── app.py
│   └── .streamlit/
│       └── secrets.toml
│
├── sql/
│   └── queries.sql
│
├── requirements.txt
├── README.md
├── .gitignore
```

---

## ⚙️ Tech Stack

* **Language:** Python
* **Database:** MySQL
* **Visualization:** Streamlit

### 📚 Libraries

* pandas
* requests
* mysql-connector-python
* streamlit
* python-dotenv

---

## 🔑 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Tushar-Chaudhari-04/Game-Analytics-Unlocking-Tennis-Data-with-SportRadar-API.git
cd Game-Analytics-Tennis
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Secrets

Create the file:

```
app/.streamlit/secrets.toml
```

Add:

```toml
[database]
host = "127.0.0.1"
user = "root"
password = "your_password"
database = "sports_db"

[api]
key = "your_sportradar_api_key"
```

---

### 5️⃣ Setup Database

```sql
CREATE DATABASE sports_db;
```

Run SQL scripts from:

```
/sql/queries.sql
```

---

### 6️⃣ Run ETL Pipeline

```bash
python etl/main.py
```

---

### 7️⃣ Run Streamlit App

```bash
python -m streamlit run app/app.py
```

---

## 📊 Features

* 📡 API Data Extraction
* 🔄 ETL Pipeline (Extract, Transform, Load)
* 🗄️ MySQL Data Storage
* 🔍 SQL-based Analysis
* 📈 Interactive Dashboard

---

## 📌 Sample Analysis

* Venue-level insights
* Competition analysis
* Country-wise distribution
* Match statistics

---

## 🚀 Demo Walkthrough

1. Run ETL pipeline to fetch and store data
2. Launch Streamlit dashboard
3. Apply filters (competition, venue, country)
4. Analyze KPIs and charts
5. Explore insights interactively

---

## 🔐 Security

* Credentials stored securely using `secrets.toml`
* Sensitive files excluded via `.gitignore`

---

## 🔮 Future Enhancements

* Player-level analytics
* Machine learning predictions
* Power BI dashboard integration
* Cloud deployment

---

## 👨‍💻 Author

**Tushar Pundlik Chaudhari**
Data Analyst | Python | SQL | Power BI

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

---

# ✅ requirements.txt (Clean & Sufficient)

```txt
pandas
requests
mysql-connector-python
streamlit
python-dotenv