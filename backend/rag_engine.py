# backend/rag_engine.py

import os
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

KNOWLEDGE_CHUNKS = [
    "Campaign targeting uses demographic filters such as age, gender, income level, and location to reach the right audience.",
    "Behavioral targeting analyzes user activity like browsing history, purchase behavior, and app usage to personalize ads.",
    "Lookalike audiences are built by finding users who share traits with your best existing customers using ML similarity models.",
    "A/B testing campaigns helps compare two versions of an ad to determine which performs better based on click-through rate and conversions.",
    "Retargeting campaigns re-engage users who previously interacted with a product but did not convert.",
    "Predictive models use features like recency, frequency, and monetary value (RFM) to score customer likelihood to convert.",
    "Campaign budget optimization automatically distributes ad spend across audience segments based on predicted ROI.",
    "Contextual targeting places ads based on the content of the web page being viewed, not the user's personal data.",
    "Geographic targeting allows campaigns to be shown only in specific cities, regions, or countries.",
    "Interest-based targeting groups users by hobbies and interests inferred from their online activity.",
    "Frequency capping limits how many times a single user sees the same ad to prevent ad fatigue.",
    "Conversion tracking measures the number of users who completed a desired action after seeing a campaign ad.",
    "Customer segmentation divides a customer base into groups based on shared characteristics for personalized campaigns.",
    "Machine learning models like Random Forest and XGBoost are used to predict campaign click-through rates.",
    "SHAP values explain which features most influenced a model's prediction for campaign targeting decisions.",
    "Campaign performance metrics include CTR, CPC, ROAS, and CPA.",
    "Natural language processing is used to analyze ad copy and match it with user intent signals.",
    "Multi-touch attribution assigns credit to multiple touchpoints in a customer journey rather than just the last click.",
    "Audience suppression prevents showing ads to users who already converted to avoid wasted budget.",
    "Real-time bidding uses automated auctions to buy ad impressions instantly based on targeting criteria.",
]

# ── Load embedder directly (avoids broken ChromaDB wrapper) ──────────────────────
print("Loading sentence transformer...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="campaign_knowledge")

if collection.count() == 0:
    print("Building vector index...")
    embeddings = embedder.encode(KNOWLEDGE_CHUNKS).tolist()
    collection.add(
        documents=KNOWLEDGE_CHUNKS,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(KNOWLEDGE_CHUNKS))]
    )
    print(f"Indexed {len(KNOWLEDGE_CHUNKS)} chunks.")

def query_rag(user_question: str, top_k: int = 4) -> str:
    query_embedding = embedder.encode([user_question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    retrieved_chunks = results["documents"][0]
    context = "\n".join([f"- {chunk}" for chunk in retrieved_chunks])

    prompt = f"""You are a campaign targeting assistant with expert knowledge in digital marketing and ML-driven ad targeting.

Use ONLY the context below to answer the user's question. If the answer is not in the context, say "I don't have enough information on that."

Context:
{context}

User Question: {user_question}

Answer:"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    print(query_rag("How does retargeting work?"))