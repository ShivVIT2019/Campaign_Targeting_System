# 🎯 AI-Powered Campaign Targeting System

An end-to-end machine learning system that predicts online shopper purchase probability to enable data-driven campaign targeting — achieving 30× ROI improvement over random selection in simulated A/B testing.

**Live Demo:** [shivvit2019.github.io/Campaign_Targeting_System](https://shivvit2019.github.io/Campaign_Targeting_System/)

---

## What It Does

Given a visitor's session behavior (pages viewed, time spent, traffic source, region, etc.), the system predicts whether they are likely to make a purchase and recommends whether to target them with an ad campaign.

Each prediction includes real-time market intelligence pulled live from the web via the [Tavily Search API](https://tavily.com/) — grounding decisions in current market trends rather than static training data alone.

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
- **Vector RAG** — ChromaDB + sentence-transformers (all-MiniLM-L6-v2) for semantic retrieval
- **RAG Evaluation** — ROUGE-L and cosine similarity scoring across 20 test questions
- **Intent Classification** — DistilBERT fine-tuned with LoRA/PEFT on campaign intent queries

---

## Tech Stack

### Backend
- **FastAPI** — 8 RESTful endpoints
- **scikit-learn** — Random Forest classifier
- **ChromaDB** — vector database for semantic retrieval
- **sentence-transformers** (`all-MiniLM-L6-v2`) — embedding model for RAG
- **Tavily Python SDK** — real-time market context enrichment
- **Google Gemini** (`gemini-1.5-flash`) — AI assistant via RAG
- **Deployed on Google Cloud**

### ML / Evaluation
- **LoRA / PEFT** — parameter-efficient fine-tuning of DistilBERT for intent classification
- **ROUGE-L + cosine similarity** — RAG answer quality evaluation
- **Hugging Face Transformers** — model loading and training

### Frontend
- **React + Vite**
- **Axios**
- **Deployed on GitHub Pages**

---

## Project Structure

```
Campaign_Targeting_System/
├── backend/
│   ├── main.py                 # FastAPI app + all endpoints
│   ├── rag_engine.py           # Vector RAG with ChromaDB + sentence-transformers
│   ├── eval_rag.py             # RAG evaluation (ROUGE-L + semantic similarity)
│   ├── tavily_enrichment.py    # Tavily real-time search integration
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── AIAssistant.jsx
│       ├── LiveMetrics.jsx
│       ├── BatchUpload.jsx
│       └── ABTestSimulator.jsx
└── ml/
    ├── finetune_intent.py      # DistilBERT LoRA fine-tuning + benchmark
    ├── artifacts/model.joblib  # Trained Random Forest model
    └── data/                   # Training dataset
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check + model status |
| POST | `/predict` | Single prediction + market context |
| POST | `/predict-batch` | Batch CSV predictions |
| POST | `/simulate-ab-test` | A/B test simulation |
| GET | `/metrics` | Model performance metrics |
| GET | `/live-metrics` | Real-time prediction stats |
| GET | `/history` | Recent prediction history |
| POST | `/chat` | AI assistant (Gemini + Vector RAG) |

---

## Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add TAVILY_API_KEY and GEMINI_API_KEY
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` for the UI or `http://localhost:8000/docs` for the API playground.

### Run RAG Evaluation
```bash
cd backend
python eval_rag.py
# Outputs: eval_results.json
```

### Run Intent Fine-Tuning Benchmark
```bash
cd ml
python finetune_intent.py
# Outputs: finetune_benchmark.json
```

---

## Deploying to Google Cloud

### Pull latest code and restart

```bash
# SSH into your VM
gcloud compute ssh <your-vm-name> --zone=<your-zone>

# Pull latest
cd Campaign_Targeting_System
git pull origin main

# Install any new packages
cd backend
pip install -r requirements.txt

# Restart service (if using systemd)
sudo systemctl restart campaign-targeting

# Or run directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Check status
```bash
sudo systemctl status campaign-targeting
curl http://localhost:8000/health
```

---

## Environment Variables

```
TAVILY_API_KEY=tvly-dev-...
GEMINI_API_KEY=...
```

---

## How the Vector RAG Works

On startup, 20 campaign knowledge chunks are embedded using `all-MiniLM-L6-v2` and stored in ChromaDB. When a user asks a question:

1. The question is embedded with the same model
2. ChromaDB retrieves the top-4 most semantically similar chunks
3. Retrieved context is passed to Gemini with a grounded prompt
4. Gemini generates a factual, context-bound answer

---

## RAG Evaluation

| Metric | Description |
|---|---|
| ROUGE-L | Longest common subsequence overlap |
| Cosine Similarity | Semantic similarity to reference answer |

---

## Intent Classification Benchmark

| Setup | F1 Score |
|---|---|
| Zero-shot DistilBERT | ~0.33 |
| LoRA Fine-tuned | ~0.85+ |
