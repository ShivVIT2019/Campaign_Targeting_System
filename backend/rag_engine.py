import os
from google import generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

CAMPAIGN_KNOWLEDGE = """
The Campaign Targeting System uses a Random Forest classifier trained on 12,330 online shopping sessions with 89.32% AUC-ROC score. Base conversion rate is 15.47%.

Features: Administrative pages, Informational pages, ProductRelated pages and durations, BounceRates, ExitRates, PageValues, SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType, VisitorType, Weekend.

PageValues is the strongest predictor. High ProductRelated duration = high intent. High BounceRates/ExitRates = low intent. Returning visitors convert better. November/December have highest conversions.

Confidence tiers: HIGH (probability > 0.70), MEDIUM (0.50-0.70), LOW (< 0.50).

Business impact: 76% ad spend reduction, 74% buyer retention, ~30x ROI over random selection.

A/B testing compares: ML Model vs Random Selection vs Target Everyone vs Target No One. Cost per contact $1, revenue per conversion $50.

Risk score: distance from 0.5 threshold * 100. Lower = more confident decision.
"""

def answer_question(question: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""You are an AI assistant for the Campaign Targeting System. 
Answer questions using this knowledge base:

{CAMPAIGN_KNOWLEDGE}

Question: {question}

Give a clear, concise answer."""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process that question. Error: {str(e)}"
