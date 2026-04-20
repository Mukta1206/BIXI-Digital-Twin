# 🚲 BIXI Digital Twin – Smart Bike Sharing Simulation

A smart mobility and digital twin project built using real Montreal BIXI station data, Python analytics, and simulation modeling.

This project helps analyze bike availability, station congestion, demand imbalance, and rebalancing strategies for an urban bike-sharing network.

---

## 📌 Project Overview

The BIXI Digital Twin replicates real-world bike station operations and allows decision-makers to simulate how bikes move across stations during the day.

It supports smarter planning through:

- Demand monitoring
- Bike shortage detection
- Overflow prediction
- Rebalancing recommendations
- KPI dashboards
- Scenario testing

---

## 🛠 Technologies Used

- Python
- Pandas
- Streamlit / Dashboard UI
- AnyLogic Simulation
- CSV / Excel Data
- Jupyter Notebook
- Data Visualization

---

## 📊 Key Features

### 🚴 Real Station Data Integration
Uses BIXI station datasets for realistic analysis.

### 📈 KPI Dashboard
Tracks:
- Bikes available
- Empty stations
- Full stations
- Utilization trends
- Rebalancing need

### 🔁 Smart Rebalancing Logic
Detects low-stock and high-stock stations and suggests bike movement.

### 🧠 Digital Twin Simulation
Represents station behavior dynamically using simulation logic.

### 📉 Decision Support
Helps optimize operations and improve rider experience.

---

## 📂 Project Files

- `bixiapp.py` → Main dashboard app
- `BikeSharingSimulation.alp` → AnyLogic model
- `bixi_digital_twin.ipynb` → Data analysis notebook
- `bixi_stations.csv` → Dataset

---

## ▶️ How to Run

### Python App

```bash
pip install streamlit pandas
streamlit run bixiapp.py