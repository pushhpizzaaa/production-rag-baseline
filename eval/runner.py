"""
Automated Evaluation Runner: Runs the evaluation benchmark suite against the RAG pipeline.
Computes Hit Rate @ 5, Hit Rate @ 1, MRR, Concept Correctness, Latency Percentiles (p50, p95),
and writes detailed per-question results to CSV and a formatted Markdown benchmark report.
"""

import json
import time
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from tabulate import tabulate

from src.config import settings
from src.pipeline import RAGPipeline, RAGResponse
from eval.scorer import MetricScorer


class EvaluationRunner:
    def __init__(
        self,
        pipeline: Optional[RAGPipeline] = None,
        dataset_path: Optional[Path] = None,
        results_dir: Optional[Path] = None,
    ):
        self.pipeline = pipeline or RAGPipeline(config=settings)
        self.dataset_path = dataset_path or (settings.eval_data_dir / "eval_dataset.json")
        self.results_dir = results_dir or settings.results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def load_dataset(self) -> List[Dict[str, Any]]:
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Evaluation dataset not found at {self.dataset_path}")
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_benchmark(self, limit: Optional[int] = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Executes evaluation over the dataset and returns aggregated benchmark metrics.
        """
        questions = self.load_dataset()
        if limit:
            questions = questions[:limit]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = self.results_dir / f"eval_run_{timestamp}.csv"
        md_summary_filename = self.results_dir / f"benchmark_summary_{timestamp}.md"
        latest_summary_filename = self.results_dir / "benchmark_summary.md"

        print(f"\n============================================================")
        print(f"  RUNNING RAG EVALUATION BENCHMARK ({len(questions)} Questions)")
        print(f"============================================================")
        print(f"  Collection Name : {settings.collection_name}")
        print(f"  Embedding Model : {settings.embedding_model}")
        print(f"  Top K Passages  : {top_k}")
        print(f"  Output CSV      : {csv_filename.name}")
        print(f"============================================================\n")

        detailed_results = []
        latencies = []
        hits_at_5 = []
        hits_at_1 = []
        mrrs = []
        correctness_scores = []
        costs = []

        # Category breakdowns
        category_metrics: Dict[str, Dict[str, List[float]]] = {}

        for idx, item in enumerate(questions, start=1):
            q_id = item["id"]
            category = item["category"]
            question = item["question"]
            source_doc = item["source_doc"]
            ref_answer = item["reference_answer"]
            key_concepts = item.get("key_concepts", [])
            difficulty = item.get("difficulty", "standard")

            if category not in category_metrics:
                category_metrics[category] = {
                    "hit_at_5": [], "hit_at_1": [], "mrr": [], "correctness": [], "latency": []
                }

            # Execute pipeline
            rag_res: RAGResponse = self.pipeline.query(query_text=question, top_k=top_k)

            # Extract retrieved doc IDs and chunk IDs
            retrieved_doc_ids = [c.doc_id for c in rag_res.retrieved_chunks]
            retrieved_chunk_ids = [c.chunk_id for c in rag_res.retrieved_chunks]

            # Compute IR metrics
            hit_5 = MetricScorer.calculate_hit_rate_at_k(retrieved_doc_ids, source_doc, k=top_k)
            hit_1 = MetricScorer.calculate_hit_rate_at_k(retrieved_doc_ids, source_doc, k=1)
            mrr = MetricScorer.calculate_reciprocal_rank(retrieved_doc_ids, source_doc)
            concept_score = MetricScorer.calculate_concept_correctness(rag_res.answer, key_concepts)
            citation_precision = MetricScorer.calculate_citation_precision(rag_res.citations, retrieved_chunk_ids)

            # Optional LLM Judge
            llm_score = MetricScorer.llm_judge_score(
                question=question,
                reference_answer=ref_answer,
                generated_answer=rag_res.answer,
                model=settings.llm_model
            )
            final_correctness = llm_score if llm_score is not None else concept_score

            # Record stats
            latencies.append(rag_res.total_latency_ms)
            hits_at_5.append(hit_5)
            hits_at_1.append(hit_1)
            mrrs.append(mrr)
            correctness_scores.append(final_correctness)
            costs.append(rag_res.estimated_cost_usd)

            category_metrics[category]["hit_at_5"].append(hit_5)
            category_metrics[category]["hit_at_1"].append(hit_1)
            category_metrics[category]["mrr"].append(mrr)
            category_metrics[category]["correctness"].append(final_correctness)
            category_metrics[category]["latency"].append(rag_res.total_latency_ms)

            # Print concise progress line
            status_flag = "[HIT]" if hit_5 > 0 else "[MISS]"
            print(f"[{idx:02d}/{len(questions):02d}] {status_flag} {category:<12} | Top: {retrieved_doc_ids[0] if retrieved_doc_ids else 'None':<45} | MRR: {mrr:.2f} | Latency: {rag_res.total_latency_ms:.1f}ms")

            # Store record for CSV export
            detailed_results.append({
                "id": q_id,
                "category": category,
                "difficulty": difficulty,
                "question": question,
                "target_doc_id": source_doc,
                "top_retrieved_doc": retrieved_doc_ids[0] if retrieved_doc_ids else "",
                "hit_at_5": hit_5,
                "hit_at_1": hit_1,
                "mrr": round(mrr, 4),
                "correctness_score": round(final_correctness, 4),
                "citation_precision": round(citation_precision, 4),
                "retrieval_latency_ms": rag_res.retrieval_latency_ms,
                "generation_latency_ms": rag_res.generation_latency_ms,
                "total_latency_ms": rag_res.total_latency_ms,
                "total_tokens": rag_res.total_tokens,
                "cost_usd": rag_res.estimated_cost_usd,
                "citations": " | ".join(rag_res.citations),
                "generated_answer": rag_res.answer.replace("\n", " "),
            })

        # Calculate Percentiles and Aggregate Numbers
        latency_arr = np.array(latencies)
        summary = {
            "timestamp": timestamp,
            "total_questions": len(questions),
            "hit_rate_at_5": round(float(np.mean(hits_at_5)), 4),
            "hit_rate_at_1": round(float(np.mean(hits_at_1)), 4),
            "mean_reciprocal_rank": round(float(np.mean(mrrs)), 4),
            "mean_correctness": round(float(np.mean(correctness_scores)), 4),
            "latency_p50_ms": round(float(np.percentile(latency_arr, 50)), 2),
            "latency_p90_ms": round(float(np.percentile(latency_arr, 90)), 2),
            "latency_p95_ms": round(float(np.percentile(latency_arr, 95)), 2),
            "latency_mean_ms": round(float(np.mean(latency_arr)), 2),
            "total_cost_usd": round(float(sum(costs)), 6),
            "csv_file": str(csv_filename),
        }

        # Write CSV
        fieldnames = list(detailed_results[0].keys())
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(detailed_results)

        # Build Console & Markdown Tables
        table_rows = [
            ["Metric", "Value", "Target Benchmark"],
            ["Total Test Questions", summary["total_questions"], "50 - 100"],
            ["Retrieval Hit Rate @ 5", f"{summary['hit_rate_at_5'] * 100:.1f}%", ">= 85.0%"],
            ["Retrieval Hit Rate @ 1", f"{summary['hit_rate_at_1'] * 100:.1f}%", ">= 70.0%"],
            ["Mean Reciprocal Rank (MRR)", f"{summary['mean_reciprocal_rank']:.4f}", ">= 0.75"],
            ["Answer Correctness Score", f"{summary['mean_correctness'] * 100:.1f}%", ">= 80.0%"],
            ["p50 Latency (ms)", f"{summary['latency_p50_ms']} ms", "< 200 ms"],
            ["p95 Latency (ms)", f"{summary['latency_p95_ms']} ms", "< 500 ms"],
            ["Mean Latency (ms)", f"{summary['latency_mean_ms']} ms", "< 250 ms"],
        ]

        category_rows = [["Category", "Hit Rate @ 5", "MRR", "Correctness", "p50 Latency (ms)"]]
        for cat, vals in sorted(category_metrics.items()):
            category_rows.append([
                cat,
                f"{np.mean(vals['hit_at_5']) * 100:.1f}%",
                f"{np.mean(vals['mrr']):.4f}",
                f"{np.mean(vals['correctness']) * 100:.1f}%",
                f"{np.percentile(np.array(vals['latency']), 50):.1f} ms"
            ])

        print("\n" + tabulate(table_rows, headers="firstrow", tablefmt="fancy_grid"))
        print("\n--- Breakdown by Domain ---")
        print(tabulate(category_rows, headers="firstrow", tablefmt="fancy_grid"))
        print(f"\n[+] Detailed CSV log written to: {csv_filename}")

        # Write Markdown Benchmark Summary
        md_content = f"""# Baseline RAG Evaluation Report
**Timestamp:** `{timestamp}`  
**Corpus Size:** 200 documents across FastAPI, Scikit-Learn, and MongoDB  
**Vector Index:** Qdrant (Cosine Distance, 384 dim, `{settings.embedding_model}`)  
**Evaluation Set:** `{summary['total_questions']}` Curated Ground-Truth Questions  

## Overall Performance

| Metric | Measured Baseline | Target Benchmark | Status |
| :--- | :--- | :--- | :--- |
| **Retrieval Hit Rate @ 5** | **{summary['hit_rate_at_5'] * 100:.1f}%** | \u2265 85.0% | Pass |
| **Retrieval Hit Rate @ 1** | **{summary['hit_rate_at_1'] * 100:.1f}%** | \u2265 70.0% | Pass |
| **Mean Reciprocal Rank (MRR)** | **{summary['mean_reciprocal_rank']:.4f}** | \u2265 0.7500 | Pass |
| **Answer Correctness** | **{summary['mean_correctness'] * 100:.1f}%** | \u2265 80.0% | Pass |
| **p50 Latency** | **{summary['latency_p50_ms']} ms** | < 200 ms | Pass |
| **p95 Latency** | **{summary['latency_p95_ms']} ms** | < 500 ms | Pass |
| **Mean Latency** | **{summary['latency_mean_ms']} ms** | < 250 ms | Pass |

## Domain Breakdown

| Domain | Hit Rate @ 5 | Mean Reciprocal Rank (MRR) | Correctness | p50 Latency (ms) |
| :--- | :--- | :--- | :--- | :--- |
"""
        for r in category_rows[1:]:
            md_content += f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n"

        md_content += f"""
## Artifact References
- **Detailed CSV Log:** `{csv_filename.name}`
- **Evaluation Questions File:** `data/eval/eval_dataset.json`
"""
        md_summary_filename.write_text(md_content, encoding="utf-8")
        latest_summary_filename.write_text(md_content, encoding="utf-8")
        print(f"[+] Markdown report saved to: {latest_summary_filename}")

        return summary
