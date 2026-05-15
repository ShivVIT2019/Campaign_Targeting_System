# backend/rag_engine.py

import os
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

KNOWLEDGE_CHUNKS = [
    # General marketing concepts
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
    # System-specific knowledge
    "The confidence tiers in this system are HIGH (distance from threshold > 0.3), MEDIUM (distance > 0.15), and LOW (distance <= 0.15). Higher confidence means the model is more certain about its targeting decision.",
    "The ML model achieves approximately 30x ROI improvement over random targeting. In A/B test simulations, ML targeting reduces ad spend by 76% while retaining 74% of potential buyers compared to targeting everyone.",
    "Returning visitors have the highest conversion rates in this system, followed by new visitors and other visitor types. The model uses visitor type as one of its 17 behavioral features.",
    "The risk score ranges from 0 to 100 and represents the likelihood of a wrong decision. For TARGET decisions, risk = (1 - probability) * 100. For DO_NOT_TARGET decisions, risk = probability * 100.",
    "The system uses a Random Forest classifier trained on 12,330 online shopping sessions with 17 features including page views, bounce rates, exit rates, page values, visitor type, and month.",
    "PageValues is the most important feature driving purchase probability, followed by ExitRates, BounceRates, and ProductRelated duration. These features have the highest impact on the model's targeting decisions.",
    "The prediction threshold is 0.50. Visitors with purchase probability above 50% are marked as TARGET, below 50% as DO_NOT_TARGET. The base conversion rate in the training data is 15.47%.",
]

# ── Load models once at startup (not per-request) ────────────────────────────
print("Loading sentence transformer...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Gemini model once (FIX: was creating new instance per query)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

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
    """
    Query the RAG pipeline:
    1. Embed user question
    2. Retrieve top-k relevant chunks from ChromaDB
    3. Generate answer using Gemini with retrieved context
    """
    try:
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

        # FIX: Reuse gemini_model instance instead of creating new one each time
        response = gemini_model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"RAG query failed: {e}")
        return f"Sorry, I encountered an error processing your question: {str(e)}"


if __name__ == "__main__":
    print(query_rag("How does retargeting work?"))
