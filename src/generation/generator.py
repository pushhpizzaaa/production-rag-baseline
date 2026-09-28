"""
RAG Generator: Assembles grounded context prompts, generates answers with strict citations
([Doc: <doc_id>#<chunk_id>]), handles LiteLLM completions, and provides an offline
deterministic grounded synthesizer when external LLM API keys are omitted.
"""

import time
import re
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.retrieval.retriever import RetrievalHit


class GenerationResult(BaseModel):
    answer: str
    citations: List[str]
    model: str
    generation_latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float


class RAGGenerator:
    SYSTEM_PROMPT = (
        "You are an expert technical assistant. Your task is to provide accurate, grounded answers "
        "to technical questions using ONLY the provided documentation context chunks.\\n\\n"
        "STRICT INSTRUCTIONS:\\n"
        "1. Every factual statement or code recommendation must cite its source chunk using the exact format: "
        "`[Doc: <chunk_id>]`. Example: `FastAPI validates types using Pydantic [Doc: fastapi_path_parameters_and_types#chunk_0]`.\\n"
        "2. Do not invent information or cite documents that are not in the context.\\n"
        "3. If the context does not contain sufficient details to fully answer, state what is known from the context "
        "and note that the remaining details are missing from the corpus."
    )

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        openai_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
    ):
        self.model = model
        self.temperature = temperature
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        if gemini_api_key:
            os.environ["GEMINI_API_KEY"] = gemini_api_key
        if anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

    def _has_active_api_key(self) -> bool:
        """Checks if any recognized LLM API key is present in environment."""
        keys = ["OPENAI_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY", "GROQ_API_KEY"]
        return any(os.environ.get(k) and os.environ.get(k).strip() != "" for k in keys)

    def _build_context_prompt(self, hits: List[RetrievalHit]) -> str:
        """Formats retrieved chunks into clear, cited context blocks."""
        blocks = []
        for i, hit in enumerate(hits, start=1):
            blocks.append(
                f"--- CONTEXT CHUNK {i} ---\\n"
                f"Source Chunk ID: {hit.chunk_id}\\n"
                f"Document: {hit.title} ({hit.category})\\n"
                f"Content:\\n{hit.text}\\n"
            )
        return "\\n".join(blocks)

    def _extract_citations(self, text: str) -> List[str]:
        """Extracts unique cited chunk IDs matching `[Doc: <chunk_id>]`."""
        matches = re.findall(r"\[Doc:\s*([^\]]+)\]", text)
        cleaned = []
        for m in matches:
            cleaned_m = m.strip().replace("`", "")
            if cleaned_m not in cleaned:
                cleaned.append(cleaned_m)
        return cleaned

    def _offline_grounded_synthesize(self, query: str, hits: List[RetrievalHit]) -> str:
        """
        Deterministic, offline grounded synthesis.
        Extracts salient grounded facts from the top chunks with valid citations.
        Ensures zero-cost offline reproduction and CI testing without external API calls.
        """
        if not hits:
            return "No relevant documentation chunks were retrieved to answer the question."

        primary_hit = hits[0]
        # Clean text lines from chunk
        lines = [line.strip() for line in primary_hit.text.splitlines() if line.strip()]
        
        # Filter out markdown headers for summary extraction
        body_lines = [l for l in lines if not l.startswith("#") and not l.startswith("[")]
        summary_snippet = " ".join(body_lines[:3]) if body_lines else primary_hit.text[:200]

        answer_parts = [
            f"Based on `{primary_hit.title}` ({primary_hit.category}):",
            f"{summary_snippet} [Doc: {primary_hit.chunk_id}].",
        ]

        # Add secondary supporting citation if available
        if len(hits) > 1:
            sec_hit = hits[1]
            sec_lines = [l for l in sec_hit.text.splitlines() if l.strip() and not l.startswith("#") and not l.startswith("[")]
            sec_snippet = " ".join(sec_lines[:2]) if sec_lines else sec_hit.text[:150]
            answer_parts.append(
                f"Furthermore, `{sec_hit.title}` explains that: {sec_snippet} [Doc: {sec_hit.chunk_id}]."
            )

        return "\\n\\n".join(answer_parts)

    def generate(self, query: str, hits: List[RetrievalHit]) -> GenerationResult:
        """
        Executes answer generation with citations. Uses LiteLLM if API keys are set;
        otherwise runs grounded offline synthesis.
        """
        start_time = time.perf_counter()
        context_block = self._build_context_prompt(hits)

        user_content = (
            f"CONTEXT INFORMATION:\\n{context_block}\\n\\n"
            f"QUESTION: {query}\\n\\n"
            f"Please answer the question accurately using ONLY the above context, "
            f"citing every fact with [Doc: <chunk_id>]."
        )

        use_litellm = self._has_active_api_key()

        if use_litellm:
            try:
                import litellm
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_content}
                ]
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature
                )
                raw_answer = response.choices[0].message.content
                prompt_tokens = response.usage.prompt_tokens if hasattr(response, "usage") else len(user_content.split()) * 1.3
                completion_tokens = response.usage.completion_tokens if hasattr(response, "usage") else len(raw_answer.split()) * 1.3
                model_used = self.model
                # Approximate cost (e.g. gpt-4o-mini is ~$0.15/1M in, $0.60/1M out)
                est_cost = (prompt_tokens * 0.00000015) + (completion_tokens * 0.00000060)
            except Exception as e:
                # Fallback to offline synthesis if network/quota error occurs
                raw_answer = f"{self._offline_grounded_synthesize(query, hits)}\\n\\n*(Fallback note: LLM API returned {str(e)[:60]})*"
                prompt_tokens = int(len(user_content.split()) * 1.33)
                completion_tokens = int(len(raw_answer.split()) * 1.33)
                model_used = "offline-grounded-fallback"
                est_cost = 0.0
        else:
            raw_answer = self._offline_grounded_synthesize(query, hits)
            prompt_tokens = int(len(user_content.split()) * 1.33)
            completion_tokens = int(len(raw_answer.split()) * 1.33)
            model_used = "offline-grounded-synthesizer"
            est_cost = 0.0

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        citations = self._extract_citations(raw_answer)

        # Safety: If generation forgot citations but had hits, attach the top hit
        if not citations and hits:
            citations = [hits[0].chunk_id]
            if f"[Doc: {hits[0].chunk_id}]" not in raw_answer:
                raw_answer += f" [Doc: {hits[0].chunk_id}]"

        return GenerationResult(
            answer=raw_answer,
            citations=citations,
            model=model_used,
            generation_latency_ms=round(latency_ms, 2),
            prompt_tokens=int(prompt_tokens),
            completion_tokens=int(completion_tokens),
            total_tokens=int(prompt_tokens + completion_tokens),
            estimated_cost_usd=round(est_cost, 6)
        )
