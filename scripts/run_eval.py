"""
CLI Entry Point: Execute Automated RAG Evaluation Benchmark.
Usage:
    python scripts/run_eval.py [--limit 10] [--top-k 5]
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from eval.runner import EvaluationRunner


def main():
    parser = argparse.ArgumentParser(description="Run RAG Evaluation Benchmark Suite.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of evaluation questions to run.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of retrieved context passages.")
    args = parser.parse_args()

    runner = EvaluationRunner()
    try:
        runner.run_benchmark(limit=args.limit, top_k=args.top_k)
    finally:
        runner.pipeline.vector_store.close()


if __name__ == "__main__":
    main()
