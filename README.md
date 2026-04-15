⚡ EV Intelligence Hub
A professional Electric Vehicle Analytics Dashboard built with Python & Streamlit — featuring interactive filters, KPI cards, and dynamic visualisations in a dark corporate UI.

📌 Overview
EV Intelligence Hub analyses 279K+ EV registration records from Washington State Department of Licensing (DOL) and converts raw data into actionable insights through charts, KPIs, and filters.

🎯 Objectives
Perform EDA on real-world EV dataset
Build an interactive dashboard (Streamlit)
Identify EV adoption trends
Forecast future growth (2025–2027) using regression

📁 Project Structure
ev_dashboard/
│
├── app.py                     # Main application (Flask/Streamlit entry point)
├── generate_charts.py         # Script to generate all charts
│
├── data/
│   └── Electric_Vehicle_Population_Data.csv   # Dataset
│
├── charts/                   # Generated visualization images
│
├── static/                 
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
│
├── templates/            
│   └── index.html
|
├── README.md                 

🚀 Setup
git clone https://github.com/vishwjeetchakrwarti/ev-intelligence-hub.git
cd ev-intelligence-hub
pip install -r requirements.txt
streamlit run app.py

🧹 Data Processing
Removed duplicates & invalid entries
Handled missing values
Standardised columns
Created range categories & EV type groups

📊 Key Features
🔢 KPI Cards (Total EVs, Avg Range, BEV Share)
📈 6+ Interactive Charts (Growth, Brands, Range, Cities)
🎛️ Dynamic Filters (City, EV Type, Year)
🌙 Dark-themed professional UI

👤 Author 
"Vishwjeet Chakrwarti" Connect on LinkedIn

