# 🎾 Game Analytics: Tennis Data Pipeline & Dashboard

## 🔥 Key Highlights
- Modular Architecture (ETL + App Separation)
- End-to-End Data Pipeline (API → MySQL → Dashboard)
- Real-world Sports Analytics Use Case
- Secure Credential Handling using Streamlit Secrets

---

## 📌 Project Overview

This project focuses on building a complete **data analytics pipeline for tennis data** using API integration, database storage, and interactive visualization.

The system extracts data from external APIs, processes it using ETL pipelines, stores it in MySQL, and presents insights through a Streamlit dashboard.

---

## 🎯 Objectives

- Extract tennis data from API
- Transform and clean data using ETL process
- Load structured data into MySQL database
- Perform SQL-based analysis
- Build an interactive dashboard using Streamlit

---

## 🏗️ Architecture
API → ETL Pipeline → MySQL Database → Streamlit Dashboard


---

## 📂 Project Structure


Game-Analytics-Tennis/
│
├── etl/ # Data extraction + transformation
│ ├── extract/api_client + extractor.py
│ ├── transform/transformer.py
│ └── load/db.py+loader.py
│ └── config.py
  └── main.py
  └── requirements.txt
 
├── app/ # Streamlit app
│ ├── app.py
│ └── .streamlit/secrets.toml
│
├── sql/
│ └── queries.sql
│
├── requirements.txt
├── README.md
├── .gitignore


---

## ⚙️ Tech Stack

- **Language:** Python
- **Database:** MySQL
- **Visualization:** Streamlit
- **Libraries:**
  - pandas
  - requests
  - mysql-connector-python
  - streamlit
  - python-dotenv

---

## 🔑 Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Tushar-Chaudhari-04/Game-Analytics-Unlocking-Tennis-Data-with-SportRadar-API.git
cd Game-Analytics-Tennis
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Secrets

Create file:

.streamlit/secrets.toml

Add:

[database]
host = "127.0.0.1"
user = "root"
password = "your_password"
database = "sports_db"

[api]
key = "your_sportradar_api_key"
5️⃣ Setup Database
CREATE DATABASE sports_db;

Run SQL scripts from /sql/queries.sql

6️⃣ Run ETL Pipeline
python etl/main.py

7️⃣ Run Streamlit App
python -m streamlit run app/app.py

📊 Features
📡 API Data Extraction
🔄 ETL Pipeline (Extract, Transform, Load)
🗄️ MySQL Data Storage
🔍 SQL Analytics
📈 Interactive Dashboard
📌 Sample Analysis
Venue-level insights
Competition analysis
Country-wise distribution
Match statistics
🚀 Demo Walkthrough
Run ETL pipeline to fetch and store data
Launch Streamlit dashboard
Apply filters (competition, venue, country)
Analyze KPIs and charts
Explore insights interactively
🔐 Security
Credentials stored securely in .streamlit/secrets.toml
.gitignore prevents sensitive data from being committed
🔮 Future Enhancements
Player-level analytics
Machine learning predictions
Power BI dashboard integration
Cloud deployment

👨‍💻 Author
Tushar Chaudhari
Data Analyst | Python | SQL | Power BI

⭐ Support

If you like this project, give it a ⭐ on GitHub!


---

# ✅ 2. requirements.txt (Clean & Sufficient)

```txt
pandas
requests
mysql-connector-python
streamlit
python-dotenv