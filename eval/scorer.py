"""
Evaluation Scorer: Implements formal information retrieval (IR) metrics and answer correctness scoring.
Metrics:
- Hit Rate @ k (Hit@5, Hit@1)
- Mean Reciprocal Rank (MRR)
- Concept Coverage & Answer Correctness
- Citation Precision
"""

from typing import List, Dict, Any, Optional
import re
import os


class MetricScorer:
    @staticmethod
    def calculate_hit_rate_at_k(retrieved_doc_ids: List[str], target_doc_id: str, k: int = 5) -> float:
        """Returns 1.0 if target_doc_id appears in top k retrieved document IDs, else 0.0."""
        top_k_ids = retrieved_doc_ids[:k]
        return 1.0 if target_doc_id in top_k_ids else 0.0

    @staticmethod
    def calculate_reciprocal_rank(retrieved_doc_ids: List[str], target_doc_id: str) -> float:
        """Returns 1 / rank (1-indexed) of the first occurrence of target_doc_id, or 0.0."""
        for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
            if doc_id == target_doc_id:
                return 1.0 / rank
        return 0.0

    @staticmethod
    def calculate_citation_precision(citations: List[str], retrieved_chunk_ids: List[str]) -> float:
        """Verifies if the cited chunks actually came from the retrieved set."""
        if not citations:
            return 0.0
        valid_citations = [c for c in citations if c in retrieved_chunk_ids]
        return len(valid_citations) / len(citations)

    @staticmethod
    def calculate_concept_correctness(answer: str, key_concepts: List[str]) -> float:
        """
        Calculates semantic factual concept coverage (0.0 to 1.0).
        Evaluates presence of expected technical terms in the generated answer.
        """
        if not key_concepts:
            return 1.0
        answer_lower = answer.lower()
        matched = 0
        for concept in key_concepts:
            # Word boundary or case-insensitive phrase match
            pattern = re.escape(concept.lower())
            if re.search(pattern, answer_lower):
                matched += 1
        return round(matched / len(key_concepts), 3)

    @staticmethod
    def llm_judge_score(
        question: str,
        reference_answer: str,
        generated_answer: str,
        model: str = "gpt-4o-mini"
    ) -> Optional[float]:
        """
        Invokes an LLM Judge via LiteLLM to score factual correctness from 0.0 to 1.0
        if an external API key is active.
        """
        has_key = any(os.environ.get(k) for k in ["OPENAI_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY"])
        if not has_key:
            return None

        try:
            import litellm
            prompt = (
                f"You are an impartial academic evaluator scoring a technical RAG system.\\n\\n"
                f"Question: {question}\\n"
                f"Reference Ground-Truth Answer: {reference_answer}\\n"
                f"Generated Answer: {generated_answer}\\n\\n"
                f"Task: Rate the factual correctness of the Generated Answer compared to the Reference Answer.\\n"
                f"Output ONLY a single floating-point number between 0.0 and 1.0 (e.g. 0.95), where:\\n"
                f"1.0 = Completely accurate and contains all critical technical facts\\n"
                f"0.5 = Partially correct but misses key nuances\\n"
                f"0.0 = Factually contradictory, completely hallucinated, or irrelevant."
            )
            res = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            raw = res.choices[0].message.content.strip()
            score_match = re.search(r"(\d+(\.\d+)?)", raw)
            if score_match:
                score = float(score_match.group(1))
                return min(max(score, 0.0), 1.0)
        except Exception:
            return None
        return None
