# 🎯 Campaign Targeting System

AI-powered purchase probability prediction for smarter, data-driven marketing.

**Live Demo:** [https://shivvit2019.github.io/Campaign_Targeting_System/](https://shivvit2019.github.io/Campaign_Targeting_System/)
**Backend API:** [https://campaign-targeting-backend-405497784425.us-central1.run.app](https://campaign-targeting-backend-405497784425.us-central1.run.app)

---

## What This System Does

- **ML Predictions:** Random Forest classifier trained on 12,330 user sessions (89.32% AUC-ROC)
- **RAG AI Assistant:** Google Gemini + ChromaDB + sentence-transformers for natural language Q&A over campaign data
- **Real-time Market Enrichment:** Tavily API for live market intelligence on each prediction
- **A/B Test Simulator:** Compare ML targeting vs random selection (~30x ROI improvement)
- **Batch Processing:** Upload CSVs for bulk predictions with confidence tiers
- **Live Dashboard:** React frontend with KPI metrics, model performance, and prediction history

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | Random Forest (scikit-learn), 89.32% AUC-ROC |
| RAG Pipeline | ChromaDB + sentence-transformers + Google Gemini 2.5-flash |
| RAG Evaluation | ROUGE-L + cosine similarity (20 test cases, 4 question types) |
| Backend | FastAPI (8 REST endpoints) |
| Frontend | React + Vite |
| Real-time Data | Tavily Search API with LRU caching |
| Deployment | Google Cloud Run + Docker + CI/CD |
| Frontend Hosting | GitHub Pages |

---

## Project Structure

```
Campaign_Targeting_System/
├── backend/
│   ├── main.py                 # FastAPI app with 8 endpoints
│   ├── rag_engine.py           # RAG pipeline (ChromaDB + Gemini)
│   ├── eval_rag.py             # RAG evaluation framework
│   ├── tavily_enrichment.py    # Real-time market data enrichment
│   ├── model.joblib            # Trained ML model artifact
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container config
│   ├── .env                    # API keys (not committed)
│   └── .env.example            # Template for API keys
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app with all tabs
│   │   ├── AIAssistant.jsx     # RAG chatbot UI
│   │   └── ABTestSimulator.jsx # A/B test comparison UI
│   ├── dist/                   # Built frontend (deployed to GitHub Pages)
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## Quick Start (Local Development)

### 1. Clone and setup

```bash
git clone https://github.com/ShivVIT2019/Campaign_Targeting_System.git
cd Campaign_Targeting_System/backend
```

### 2. Create .env file

```bash
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Test endpoints

```bash
# Health check
curl http://localhost:8000/health

# Chat with AI Assistant
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is retargeting?"}'

# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"ProductRelated": 5, "BounceRates": 0.02, "ExitRates": 0.05, "PageValues": 10.0, "Month": "May", "VisitorType": "Returning_Visitor"}'

# Model metrics
curl http://localhost:8000/metrics

# Live metrics
curl http://localhost:8000/live-metrics
```

### 6. Run frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### 7. Run RAG evaluation

```bash
cd backend
python eval_rag.py
# Outputs: eval_results.json with ROUGE-L and cosine similarity scores
```

---

## Google Cloud Run Deployment

### First-time setup

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project campaign-targeting-system

# Check project ID
gcloud config get-value project
# Should return: campaign-targeting-system
```

### Build and deploy backend

```bash
cd backend

# Build Docker image in cloud
gcloud builds submit --tag gcr.io/campaign-targeting-system/campaign-targeting-backend

# Deploy to Cloud Run
gcloud run deploy campaign-targeting-backend \
  --image gcr.io/campaign-targeting-system/campaign-targeting-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=your_key,TAVILY_API_KEY=your_key" \
  --memory 4Gi \
  --cpu 2 \
  --timeout 600
```

### Test deployed backend

```bash
curl https://campaign-targeting-backend-405497784425.us-central1.run.app/health

curl -X POST https://campaign-targeting-backend-405497784425.us-central1.run.app/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is retargeting?"}'
```

### Deploy frontend to GitHub Pages

```bash
cd frontend
npm run build
cd ..
git add .
git commit -m "deploy frontend"
git push origin main
```

---

## Common Operations & Commands

### Update API keys on Cloud Run

```bash
gcloud run services update campaign-targeting-backend \
  --region us-central1 \
  --update-env-vars "GEMINI_API_KEY=new_key,TAVILY_API_KEY=new_key"
```

### Update backend URL in all frontend files

```bash
# If backend service name changes, update all frontend files:
cd frontend/src
sed -i '' 's/OLD_URL/NEW_URL/g' App.jsx
sed -i '' 's/OLD_URL/NEW_URL/g' AIAssistant.jsx
sed -i '' 's/OLD_URL/NEW_URL/g' ABTestSimulator.jsx

# Then rebuild
cd ..
npm run build
cd ..
git add .
git commit -m "update backend URL"
git push origin main
```

### List all Cloud Run services

```bash
gcloud run services list --region us-central1
```

### Delete a Cloud Run service

```bash
gcloud run services delete SERVICE_NAME --region us-central1
```

### Check which URL frontend is using

```bash
grep "campaign" frontend/src/App.jsx
grep "campaign" frontend/src/AIAssistant.jsx
grep "campaign" frontend/src/ABTestSimulator.jsx
```

### Check built files have correct URL

```bash
grep "campaign" frontend/dist/assets/*.js | head -3
```

### View Cloud Run logs

```bash
gcloud run services logs read campaign-targeting-backend --region us-central1 --limit 50
```

### Update traffic to latest revision

```bash
gcloud run services update-traffic campaign-targeting-backend \
  --region us-central1 \
  --to-latest
```

### Check current env vars on Cloud Run

```bash
gcloud run services describe campaign-targeting-backend \
  --region us-central1 \
  --format="yaml" | grep -A1 "name: GEMINI"
```

### Bake sentence-transformer model into Docker (avoids cold start)

```bash
cd backend
python3 -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')
print('Model saved locally')
"
# Then add to Dockerfile: COPY models/ ./models/
# And set: ENV SENTENCE_TRANSFORMERS_HOME=/app/models
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with model status |
| `/predict` | POST | Single prediction with market context |
| `/predict-batch` | POST | Batch predictions from CSV upload |
| `/simulate-ab-test` | POST | A/B test simulation comparing strategies |
| `/chat` | POST | RAG-powered AI Q&A assistant |
| `/metrics` | GET | Model performance metrics |
| `/live-metrics` | GET | Real-time prediction statistics |
| `/model-metrics` | GET | Detailed model metrics with ROC curve |
| `/history` | GET | Recent prediction history |

---

## Bug Fixes Applied (March 2026)

1. **requirements.txt** — Added missing: chromadb, sentence-transformers, rouge-score, torch. Fixed package name: google-genai → google-generativeai
2. **rag_engine.py** — Gemini model loaded once at startup (was creating new instance per query). Updated model from gemini-1.5-flash to gemini-2.5-flash
3. **eval_rag.py** — Added 4 question types: direct, paraphrased, out-of-scope, reasoning. Added per-type score breakdown
4. **tavily_enrichment.py** — Graceful fallback when API key missing (was crashing with ValueError)
5. **Dockerfile** — Added build-essential, uses ${PORT:-8080} for Cloud Run, upgraded to Python 3.11
6. **docker-compose.yml** — Added env_file support, healthcheck, correct port mapping
7. **ABTestSimulator.jsx + App.jsx** — Fixed API URL mismatch (was pointing to wrong Cloud Run service)
8. **Sentence-transformer model** — Baked into Docker image to avoid cold start download timeouts

---

## GCP Project Info

| Item | Value |
|------|-------|
| Project ID | campaign-targeting-system |
| Project Number | 405497784425 |
| Region | us-central1 |
| Backend Service | campaign-targeting-backend |
| Backend URL | https://campaign-targeting-backend-405497784425.us-central1.run.app |
| Frontend | GitHub Pages: shivvit2019.github.io/Campaign_Targeting_System |

---

## Built By

**Sivasai Atchyut Akella** — MS Computer Science (AI), Binghamton University
- GitHub: [ShivVIT2019](https://github.com/ShivVIT2019)
- LinkedIn: [atchyut](https://linkedin.com/in/atchyut)
- Portfolio: [portfolio-nine-rho-36.vercel.app](https://portfolio-nine-rho-36.vercel.app)
