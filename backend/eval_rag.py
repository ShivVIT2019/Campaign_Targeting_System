# backend/eval_rag.py

import json
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
from rag_engine import query_rag

# ── Evaluation Dataset ───────────────────────────────────────────────────────────
TEST_CASES = [
    {
        "question": "What is retargeting in digital campaigns?",
        "reference": "Retargeting campaigns re-engage users who previously interacted with a product but did not convert."
    },
    {
        "question": "How does behavioral targeting work?",
        "reference": "Behavioral targeting analyzes user activity like browsing history, purchase behavior, and app usage to personalize ads."
    },
    {
        "question": "What is a lookalike audience?",
        "reference": "Lookalike audiences are built by finding users who share traits with your best existing customers using ML similarity models."
    },
    {
        "question": "What is frequency capping?",
        "reference": "Frequency capping limits how many times a single user sees the same ad to prevent ad fatigue."
    },
    {
        "question": "What metrics measure campaign performance?",
        "reference": "Campaign performance metrics include CTR, CPC, ROAS, and CPA."
    },
    {
        "question": "What is A/B testing in campaigns?",
        "reference": "A/B testing campaigns helps compare two versions of an ad to determine which performs better based on click-through rate and conversions."
    },
    {
        "question": "What is geo-targeting?",
        "reference": "Geographic targeting allows campaigns to be shown only in specific cities, regions, or countries."
    },
    {
        "question": "How is customer segmentation used in marketing?",
        "reference": "Customer segmentation divides a customer base into groups based on shared characteristics for personalized campaigns."
    },
    {
        "question": "What ML models are used for campaign targeting?",
        "reference": "Machine learning models like Random Forest and XGBoost are used to predict campaign click-through rates."
    },
    {
        "question": "What is multi-touch attribution?",
        "reference": "Multi-touch attribution assigns credit to multiple touchpoints in a customer journey rather than just the last click."
    },
    {
        "question": "What is contextual targeting?",
        "reference": "Contextual targeting places ads based on the content of the web page being viewed, not the user's personal data."
    },
    {
        "question": "What is real-time bidding?",
        "reference": "Real-time bidding uses automated auctions to buy ad impressions instantly based on targeting criteria."
    },
    {
        "question": "What is audience suppression?",
        "reference": "Audience suppression prevents showing ads to users who already converted to avoid wasted budget."
    },
    {
        "question": "How are SHAP values used in targeting?",
        "reference": "SHAP values explain which features most influenced a model's prediction for campaign targeting decisions."
    },
    {
        "question": "What is interest-based targeting?",
        "reference": "Interest-based targeting groups users by hobbies and interests inferred from their online activity."
    },
    {
        "question": "What is conversion tracking?",
        "reference": "Conversion tracking measures the number of users who completed a desired action after seeing a campaign ad."
    },
    {
        "question": "What is campaign budget optimization?",
        "reference": "Campaign budget optimization automatically distributes ad spend across audience segments based on predicted ROI."
    },
    {
        "question": "What is RFM scoring?",
        "reference": "Predictive models use features like recency, frequency, and monetary value to score customer likelihood to convert."
    },
    {
        "question": "How is NLP used in advertising?",
        "reference": "Natural language processing is used to analyze ad copy and match it with user intent signals."
    },
    {
        "question": "What is demographic targeting?",
        "reference": "Campaign targeting uses demographic filters such as age, gender, income level, and location to reach the right audience."
    },
]

# ── Load Semantic Similarity Model ───────────────────────────────────────────────
print("Loading sentence transformer model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

# ── Run Evaluation ────────────────────────────────────────────────────────────────
def evaluate():
    results = []
    total_rouge = 0
    total_similarity = 0

    print(f"\nRunning evaluation on {len(TEST_CASES)} questions...\n")

    for i, case in enumerate(TEST_CASES):
        question = case["question"]
        reference = case["reference"]

        # Get RAG answer
        try:
            generated = query_rag(question)
        except Exception as e:
            generated = ""
            print(f"  [ERROR] Q{i+1}: {e}")

        # ROUGE-L score
        rouge_result = scorer.score(reference, generated)
        rouge_l = round(rouge_result["rougeL"].fmeasure, 4)

        # Semantic similarity
        ref_emb = embedder.encode(reference, convert_to_tensor=True)
        gen_emb = embedder.encode(generated, convert_to_tensor=True)
        similarity = round(float(util.cos_sim(ref_emb, gen_emb)[0][0]), 4)

        total_rouge += rouge_l
        total_similarity += similarity

        results.append({
            "question": question,
            "reference": reference,
            "generated": generated,
            "rouge_l": rouge_l,
            "semantic_similarity": similarity,
        })

        print(f"  Q{i+1}: ROUGE-L={rouge_l:.3f} | Similarity={similarity:.3f}")
        print(f"       Q: {question}")
        print(f"       A: {generated[:100]}...")
        print()

    n = len(TEST_CASES)
    avg_rouge = round(total_rouge / n, 4)
    avg_similarity = round(total_similarity / n, 4)

    summary = {
        "total_questions": n,
        "avg_rouge_l": avg_rouge,
        "avg_semantic_similarity": avg_similarity,
        "results": results,
    }

    # Save to file
    with open("eval_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 50)
    print(f"✅ Evaluation Complete!")
    print(f"   Avg ROUGE-L:           {avg_rouge}")
    print(f"   Avg Semantic Similarity: {avg_similarity}")
    print(f"   Results saved to:      eval_results.json")
    print("=" * 50)

    return summary


if __name__ == "__main__":
    evaluate()