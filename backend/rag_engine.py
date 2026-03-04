import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Knowledge base about the Campaign Targeting System ──────────────────────
CAMPAIGN_KNOWLEDGE = """
Campaign Targeting System - Knowledge Base

## Model Overview
The Campaign Targeting System uses a Random Forest classifier trained on 12,330 online shopping sessions.
The model achieves 89.32% AUC-ROC score.
The base conversion rate of the dataset is 15.47% (approximately 1 in 6 visitors make a purchase).
The model uses a decision threshold of 0.50 to classify visitors as TARGET or DO_NOT_TARGET.

## Features Used
The model uses 17 behavioral and demographic features:
- Administrative: Number of administrative pages visited
- Administrative_Duration: Time spent on administrative pages (seconds)
- Informational: Number of informational pages visited
- Informational_Duration: Time spent on informational pages (seconds)
- ProductRelated: Number of product-related pages visited
- ProductRelated_Duration: Time spent on product pages (seconds)
- BounceRates: Average bounce rate of pages visited
- ExitRates: Average exit rate of pages visited
- PageValues: Average page value of pages visited before completing a transaction
- SpecialDay: Closeness of the visit to a special day (e.g. Valentine's Day, 0-1 scale)
- Month: Month of the visit (Jan-Dec)
- OperatingSystems: Operating system used by visitor
- Browser: Browser used by visitor
- Region: Geographic region of visitor
- TrafficType: Type of traffic source
- VisitorType: Returning_Visitor, New_Visitor, or Other
- Weekend: Whether the visit occurred on a weekend (True/False)

## Confidence Tiers
- High Confidence: probability >= 0.70 → Strong TARGET signal, prioritize these users
- Medium Confidence: probability 0.50-0.70 → Moderate TARGET signal
- Low Confidence: probability < 0.50 → DO_NOT_TARGET, save ad spend

## Business Impact
- Reduces ad spend by 76% by not targeting low-intent visitors
- Retains 74% of potential buyers through targeted campaigns
- Achieves approximately 30x ROI improvement over random selection
- Targeting top 20% most likely buyers maximizes campaign efficiency

## Key Behavioral Insights
- PageValues is the strongest predictor of purchase intent
- High ProductRelated page visits with long duration = high purchase intent
- High BounceRates and ExitRates = low purchase intent
- Returning visitors convert at higher rates than new visitors
- Weekend visitors show different buying patterns than weekday visitors
- November and December show highest conversion rates (holiday shopping)
- Special day proximity increases purchase probability

## API Endpoints
- GET /health: System health check and total prediction count
- POST /predict: Single visitor purchase probability prediction
- POST /predict-batch: Batch predictions from CSV upload
- POST /simulate-ab-test: Compare ML targeting vs random vs target-all strategies
- GET /live-metrics: Real-time dashboard metrics and trends
- GET /model-metrics: Full model performance metrics (AUC, confusion matrix, ROC curve)
- GET /roi-analysis: ROI analysis at different probability thresholds
- POST /chat: AI-powered natural language Q&A about campaign analytics

## A/B Testing Framework
The system supports three strategies for comparison:
- ML Model (threshold 0.5): Only target visitors with >= 50% purchase probability
- Random Selection: Randomly target same number of visitors as ML model selects
- Target Everyone: Contact all visitors regardless of intent
- Target No One: Baseline with zero spend

## ROI Analysis
- Cost per contact: $1.00
- Revenue per conversion: $50.00
- ML model consistently outperforms random selection
- Optimal threshold varies by campaign budget constraints
- Higher threshold = fewer contacts, higher precision, lower recall

## How to Use the System
1. Enter visitor behavioral data in the prediction form
2. Get instant purchase probability score (0-100%)
3. System recommends TARGET or DO_NOT_TARGET
4. Use batch prediction for large CSV datasets
5. Run A/B test simulation to compare strategies
6. Monitor live metrics dashboard for real-time insights
"""


def build_vectorstore():
    """Build ChromaDB vector store from campaign knowledge"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([Document(page_content=CAMPAIGN_KNOWLEDGE)])

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_API_KEY
    )

    vectorstore = Chroma.from_documents(docs, embeddings)
    return vectorstore


def get_rag_chain():
    """Build and return the RAG QA chain"""
    vectorstore = build_vectorstore()

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=False
    )

    return chain


# Initialize chain once at startup
_chain = None


def get_chain():
    global _chain
    if _chain is None:
        _chain = get_rag_chain()
    return _chain


def answer_question(question: str) -> str:
    """Answer a question about the campaign targeting system"""
    try:
        chain = get_chain()
        result = chain.invoke({"query": question})
        return result["result"]
    except Exception as e:
        return f"Sorry, I couldn't process that question. Error: {str(e)}"
