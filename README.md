# AI Predictive Maintenance System

An AI-powered web application for monitoring vehicle health and predicting maintenance risk using machine learning.

## Project Overview

The system analyzes vehicle operational parameters and uses a Random Forest classification model to predict maintenance risk.

The prediction categories are:

- Low
- Medium
- High

## Features

- Vehicle health monitoring
- AI-based maintenance risk prediction
- Random Forest machine learning model
- Vehicle parameter monitoring
- Health score calculation
- Maintenance recommendations
- Flask REST API
- Interactive web dashboard

## Machine Learning Features

The model uses seven vehicle parameters:

1. Mileage
2. Temperature
3. Fuel Consumption
4. Battery Voltage
5. Engine Vibration
6. Oil Level
7. Tire Pressure

## Technology Stack

- Python
- Pandas
- Scikit-learn
- Random Forest
- Flask
- Flask-CORS
- HTML
- CSS
- JavaScript
- REST API

## System Architecture

Vehicle Data
↓
Pandas Data Processing
↓
Random Forest Model
↓
Trained Model
↓
Flask REST API
↓
JavaScript Dashboard
↓
Maintenance Risk Prediction

## Project Structure

ai-predictive-maintenance/
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   └── predictive_model.pkl
│
├── data/
│   └── vehicle_data.csv
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── .gitignore
└── README.md

## How to Run

### 1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the virtual environment

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Train the model

cd backend

python train_model.py

### 6. Start Flask

python app.py

### 7. Open the dashboard

http://127.0.0.1:5000

## Example Predictions

Vehicle 001 → Low Risk

Vehicle 002 → Medium Risk

Vehicle 003 → High Risk

## Future Improvements

- Real-time IoT sensor integration
- Database integration
- Historical vehicle health tracking
- Predictive maintenance alerts
- Interactive charts
- Deployment to a cloud platform
## Dashboard Preview

![AI Predictive Maintenance Dashboard](screenshots/dashboard.png)
### Vehicle Data

![Vehicle Data](screenshots/vehicle-data.png)
### Vehicle Data

![Vehicle Data](screenshots/vehicle-data1.png)
### Vehicle Data

![Vehicle Data](screenshots/vehicle-data2.png)
