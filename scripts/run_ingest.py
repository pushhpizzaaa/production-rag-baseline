"""
CLI Script to Ingest the 200 Technical Documentation Files into Qdrant.
Usage:
    python scripts/run_ingest.py [--no-clear]
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.config import settings
from src.pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Ingest documentation corpus into Qdrant vector store.")
    parser.add_argument("--no-clear", action="store_true", help="Do not clear existing collection before ingestion.")
    args = parser.parse_args()

    print(f"============================================================")
    print(f"  RAG BASELINE PIPELINE - CORPUS INGESTION")
    print(f"============================================================")
    print(f"  Corpus Directory : {settings.raw_data_dir}")
    print(f"  Collection Name  : {settings.collection_name}")
    print(f"  Embedding Model  : {settings.embedding_model} ({settings.embedding_dim} dim)")
    print(f"  Chunk Size       : ~{settings.chunk_size_tokens} tokens (overlap: {settings.chunk_overlap_tokens})")
    print(f"  Storage Target   : {settings.qdrant_url if settings.qdrant_url else settings.qdrant_storage_path}")
    print(f"============================================================\n")

    pipeline = RAGPipeline(config=settings)
    clear = not args.no_clear

    print("Beginning ingestion...")
    stats = pipeline.ingest_corpus(clear_existing=clear)

    print("\n--- INGESTION COMPLETE ---")
    print(f"  Documents Loaded : {stats.documents_loaded}")
    print(f"  Chunks Created   : {stats.chunks_created}")
    print(f"  Points Indexed   : {stats.points_indexed}")
    print(f"  Elapsed Time     : {stats.elapsed_seconds:.2f} seconds")
    print(f"  Breakdown by Category:")
    for cat, count in sorted(stats.categories.items()):
        print(f"    - {cat}: {count} documents")
    print("============================================================\n")

    # Close client gracefully
    pipeline.vector_store.close()


if __name__ == "__main__":
    main()
