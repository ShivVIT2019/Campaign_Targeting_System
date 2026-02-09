# 🎯 Campaign Targeting System

Production-grade ML system for predicting customer purchase probability to optimize marketing campaigns.

## 📊 Project Overview

**Problem:** Marketing teams waste budget targeting low-intent visitors.

**Solution:** ML-powered prediction system that identifies high-probability purchasers, enabling targeted campaigns with 89.3% prediction accuracy.

**Business Impact:**
- Optimize marketing spend by targeting top 20% most likely buyers
- Reduce customer acquisition cost
- Improve conversion rates through data-driven targeting

---

## 🏗️ Architecture

┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ React │────▶│ FastAPI │────▶│ ML Model │
│ Frontend │ │ Backend │ │ (Logistics) │
└─────────────┘ └──────────────┘ └─────────────┘



**Tech Stack:**
- **ML:** Python, scikit-learn, pandas, numpy
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** React, Vite, Axios
- **DevOps:** Docker, GitHub Actions, logging

---

## 📈 Model Performance

- **ROC-AUC:** 0.8932 (89.3% accuracy)
- **Dataset:** 12,330 online shopping sessions
- **Features:** 17 behavioral + demographic variables
- **Base conversion rate:** 15.47%

**Key Features:**
- Page visit patterns (Administrative, Informational, Product)
- Session duration metrics
- Bounce/Exit rates
- Visitor type & timing
- System identifiers (OS, Browser, Region)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm

### Option 1: Docker (Recommended)
```bash
docker-compose up
Backend: http://localhost:8000

Frontend: http://localhost:5173

Option 2: Manual Setup

1. Train Model


cd ml
python3 train_and_export.py


2. Start Backend


cd backend
pip3 install -r requirements.txt
uvicorn main:app --reload --port 8000


3. Start Frontend

cd frontend
npm install
npm run dev


🧪 Testing

cd backend
pip install pytest
pytest test_api.py


📁 Project Structure

Campaign_Targeting_System/
├── ml/
│   ├── data/
│   │   └── online_shoppers_intention.csv
│   ├── train_and_export.py
│   └── artifacts/
│       └── model.joblib
├── backend/
│   ├── main.py
│   ├── test_api.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── .github/workflows/ci.yml
├── docker-compose.yml
└── README.md


🎯 Use Cases
E-commerce Marketing: Target high-intent visitors with personalized offers

Campaign Optimization: Allocate ad budget to top 20% probable buyers

Customer Segmentation: Identify distinct behavioral patterns

A/B Testing: Predict which segments respond to campaigns

🛠️ Technical Highlights
Production-ready: CI/CD pipeline, Docker, logging, monitoring

Scalable: Stateless API, containerized deployment

Tested: Automated tests for API endpoints

Monitored: Request logging, prediction tracking

Type-safe: Pydantic models for request validation

📊 API Endpoints
GET /health

Health check with metrics

{
  "status": "ok",
  "model_loaded": true,
  "total_predictions": 42,
  "base_conversion_rate": 0.1547
}


POST /predict

Predict purchase probability

{
  "probability": 0.7234,
  "decision": "TARGET",
  "threshold": 0.50,
  "prediction_id": "pred_20260205_1634_42"
}

👨‍💻 Author
Sivasai Atchyuta AKella

LinkedIn: https://www.linkedin.com/in/atchyut/

Email: sakella@binghamton.edu

