# 🎯 AI-Powered Campaign Targeting System

An end-to-end machine learning system that predicts online shopper purchase probability to enable data-driven campaign targeting — achieving **30× ROI improvement** over random selection in simulated A/B testing.

**Live Demo:** [shivvit2019.github.io/Campaign_Targeting_System](https://shivvit2019.github.io/Campaign_Targeting_System/)

---

## What It Does

Given a visitor's session behavior (pages viewed, time spent, traffic source, region, etc.), the system predicts whether they are likely to make a purchase and recommends whether to target them with an ad campaign.

Each prediction now includes **real-time market intelligence** pulled live from the web via the [Tavily Search API](https://tavily.com) — grounding decisions in current market trends rather than static training data alone.

---

## Key Results

| Metric | Value |
|---|---|
| Model | Random Forest Classifier |
| Training Data | 12,330 online shopping sessions |
| AUC-ROC | 89.32% |
| Ad Spend Reduction | 76% |
| Buyer Retention | 74% |
| ROI vs Random Targeting | ~30× |

---

## Features

- **Real-time predictions** — single visitor inference with confidence tiers (High / Medium / Low)
- **Live Market Intelligence** — Tavily-powered web search enriches every prediction with current ecommerce trends
- **Batch predictions** — upload a CSV and score thousands of visitors at once
- **A/B Test Simulator** — compare ML targeting vs random selection vs target-all strategies
- **Live Metrics Dashboard** — track prediction volume, targeting rate, and confidence distribution in real time
- **AI Assistant** — Gemini-powered RAG chatbot answers questions about the model, features, and results

---

## Tech Stack

**Backend**
- FastAPI — 8 RESTful endpoints
- scikit-learn — Random Forest classifier
- Tavily Python SDK — real-time market context enrichment
- Google Gemini (gemini-2.5-flash) — AI assistant via RAG
- Deployed on Render

**Frontend**
- React + Vite
- Axios
- Deployed on GitHub Pages

---

## Project Structure

```
Campaign_Targeting_System/
├── backend/
│   ├── main.py                 # FastAPI app + all endpoints
│   ├── rag_engine.py           # Gemini RAG + Tavily knowledge enrichment
│   ├── tavily_enrichment.py    # Tavily search integration (new)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx             # Main app + Market Intel card
│       ├── AIAssistant.jsx     # Gemini chat interface
│       ├── LiveMetrics.jsx     # Real-time dashboard
│       ├── BatchUpload.jsx     # CSV batch predictions
│       └── ABTestSimulator.jsx # A/B test comparison
└── ml/
    ├── artifacts/model.joblib  # Trained Random Forest model
    └── data/                   # Training dataset
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check + Tavily status |
| POST | `/predict` | Single prediction + market context |
| POST | `/predict-batch` | Batch CSV predictions |
| POST | `/simulate-ab-test` | A/B test simulation |
| GET | `/metrics` | Model performance metrics |
| GET | `/live-metrics` | Real-time prediction stats |
| GET | `/history` | Recent prediction history |
| POST | `/chat` | AI assistant (Gemini + RAG + Tavily) |

---

## Running Locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add TAVILY_API_KEY and GEMINI_API_KEY
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` for the UI or `http://localhost:8000/docs` for the API playground.

---

## Environment Variables

```env
TAVILY_API_KEY=tvly-dev-...     # from tavily.com
GEMINI_API_KEY=...              # from Google AI Studio
```

---

## How the Tavily Integration Works

Every call to `/predict` triggers a Tavily search for real-time ecommerce trends matching the visitor's region and traffic type. Results are returned alongside the prediction as a `market_context` block and rendered in the UI as a **"Live Market Intelligence"** card.

The AI Assistant (`/chat`) also uses Tavily to augment its static knowledge base with live web data before passing context to Gemini — making answers more current and accurate.

Results are LRU-cached so repeated identical queries don't consume extra API credits.
