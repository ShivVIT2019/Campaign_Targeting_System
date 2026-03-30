# backend/eval_rag.py

import json
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
from rag_engine import query_rag

# ── Evaluation Dataset ───────────────────────────────────────────────────────────
# Mix of direct-match questions AND adversarial/out-of-scope questions
TEST_CASES = [
    # Direct knowledge base questions
    {
        "question": "What is retargeting in digital campaigns?",
        "reference": "Retargeting campaigns re-engage users who previously interacted with a product but did not convert.",
        "type": "direct"
    },
    {
        "question": "How does behavioral targeting work?",
        "reference": "Behavioral targeting analyzes user activity like browsing history, purchase behavior, and app usage to personalize ads.",
        "type": "direct"
    },
    {
        "question": "What is a lookalike audience?",
        "reference": "Lookalike audiences are built by finding users who share traits with your best existing customers using ML similarity models.",
        "type": "direct"
    },
    {
        "question": "What is frequency capping?",
        "reference": "Frequency capping limits how many times a single user sees the same ad to prevent ad fatigue.",
        "type": "direct"
    },
    {
        "question": "What metrics measure campaign performance?",
        "reference": "Campaign performance metrics include CTR, CPC, ROAS, and CPA.",
        "type": "direct"
    },
    {
        "question": "What is A/B testing in campaigns?",
        "reference": "A/B testing campaigns helps compare two versions of an ad to determine which performs better based on click-through rate and conversions.",
        "type": "direct"
    },
    {
        "question": "What is geo-targeting?",
        "reference": "Geographic targeting allows campaigns to be shown only in specific cities, regions, or countries.",
        "type": "direct"
    },
    {
        "question": "How is customer segmentation used in marketing?",
        "reference": "Customer segmentation divides a customer base into groups based on shared characteristics for personalized campaigns.",
        "type": "direct"
    },
    {
        "question": "What ML models are used for campaign targeting?",
        "reference": "Machine learning models like Random Forest and XGBoost are used to predict campaign click-through rates.",
        "type": "direct"
    },
    {
        "question": "What is multi-touch attribution?",
        "reference": "Multi-touch attribution assigns credit to multiple touchpoints in a customer journey rather than just the last click.",
        "type": "direct"
    },
    # Adversarial / paraphrased / out-of-scope questions (FIX: tests generalization)
    {
        "question": "How can I reduce wasted ad spend on users who already bought my product?",
        "reference": "Audience suppression prevents showing ads to users who already converted to avoid wasted budget.",
        "type": "paraphrased"
    },
    {
        "question": "What's the best way to show ads only in New York City?",
        "reference": "Geographic targeting allows campaigns to be shown only in specific cities, regions, or countries.",
        "type": "paraphrased"
    },
    {
        "question": "How do I stop showing the same ad too many times to one person?",
        "reference": "Frequency capping limits how many times a single user sees the same ad to prevent ad fatigue.",
        "type": "paraphrased"
    },
    {
        "question": "Can I target users based on what websites they visit without tracking them personally?",
        "reference": "Contextual targeting places ads based on the content of the web page being viewed, not the user's personal data.",
        "type": "paraphrased"
    },
    {
        "question": "What is the difference between CPC and CPM in advertising?",
        "reference": "I don't have enough information on that.",
        "type": "out_of_scope"
    },
    {
        "question": "How do I set up a Facebook Ads account?",
        "reference": "I don't have enough information on that.",
        "type": "out_of_scope"
    },
    {
        "question": "What programming language should I use for ad tech?",
        "reference": "I don't have enough information on that.",
        "type": "out_of_scope"
    },
    {
        "question": "How do I combine retargeting with lookalike audiences for better results?",
        "reference": "Retargeting re-engages previous visitors while lookalike audiences find similar new users using ML similarity models.",
        "type": "reasoning"
    },
    {
        "question": "What is the relationship between RFM scoring and customer segmentation?",
        "reference": "RFM scoring uses recency, frequency, and monetary value to score customers, which feeds into customer segmentation for personalized campaigns.",
        "type": "reasoning"
    },
    {
        "question": "How can SHAP values improve campaign budget optimization?",
        "reference": "SHAP values explain feature importance in predictions, which helps optimize budget allocation across audience segments.",
        "type": "reasoning"
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
    scores_by_type = {"direct": [], "paraphrased": [], "out_of_scope": [], "reasoning": []}

    print(f"\nRunning evaluation on {len(TEST_CASES)} questions...\n")

    for i, case in enumerate(TEST_CASES):
        question = case["question"]
        reference = case["reference"]
        q_type = case.get("type", "direct")

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

        scores_by_type[q_type].append({"rouge_l": rouge_l, "similarity": similarity})

        results.append({
            "question": question,
            "reference": reference,
            "generated": generated,
            "rouge_l": rouge_l,
            "semantic_similarity": similarity,
            "type": q_type,
        })

        print(f"  Q{i+1} [{q_type}]: ROUGE-L={rouge_l:.3f} | Similarity={similarity:.3f}")
        print(f"       Q: {question}")
        print(f"       A: {generated[:100]}...")
        print()

    n = len(TEST_CASES)
    avg_rouge = round(total_rouge / n, 4)
    avg_similarity = round(total_similarity / n, 4)

    # Calculate per-type averages
    type_summaries = {}
    for q_type, scores in scores_by_type.items():
        if scores:
            type_summaries[q_type] = {
                "count": len(scores),
                "avg_rouge_l": round(sum(s["rouge_l"] for s in scores) / len(scores), 4),
                "avg_similarity": round(sum(s["similarity"] for s in scores) / len(scores), 4),
            }

    summary = {
        "total_questions": n,
        "avg_rouge_l": avg_rouge,
        "avg_semantic_similarity": avg_similarity,
        "scores_by_type": type_summaries,
        "results": results,
    }

    # Save to file
    with open("eval_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print(f"Evaluation Complete!")
    print(f"   Overall Avg ROUGE-L:           {avg_rouge}")
    print(f"   Overall Avg Semantic Similarity: {avg_similarity}")
    print(f"\n   Breakdown by question type:")
    for q_type, stats in type_summaries.items():
        print(f"     {q_type:15s}: ROUGE-L={stats['avg_rouge_l']:.4f} | Similarity={stats['avg_similarity']:.4f} (n={stats['count']})")
    print(f"\n   Results saved to: eval_results.json")
    print("=" * 60)

    return summary


if __name__ == "__main__":
    evaluate()
