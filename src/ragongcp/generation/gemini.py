"""Gemini grounded generation (default Generator implementation).

Uses the Vertex-backed `google-genai` SDK. The model is instructed to answer
only from the numbered context passages and cite them inline as [n]; we then map
those markers back to source chunks as first-class Citations.
"""

from __future__ import annotations

from ragongcp.config import GenerationConfig, Settings
from ragongcp.domain.models import Answer, Chunk
from ragongcp.generation.prompt import build_prompt, extract_citations


class GeminiGenerator:
    def __init__(self, generation: GenerationConfig, settings: Settings) -> None:
        self.generation = generation
        self.settings = settings
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai
            except Exception as exc:  # pragma: no cover
                raise ImportError(
                    "google-genai is not installed. Install 'google-genai>=0.3'."
                ) from exc
            if not self.settings.project_id:
                raise RuntimeError("RAGONGCP_PROJECT_ID is not set — required for Gemini.")
            self._client = genai.Client(
                vertexai=True,
                project=self.settings.project_id,
                location=self.settings.location,
            )
        return self._client

    def generate(self, question: str, chunks: list[Chunk]) -> Answer:
        prompt = build_prompt(self.generation.system_prompt, question, chunks)
        client = self._get_client()

        from google.genai import types

        response = client.models.generate_content(
            model=self.generation.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.generation.temperature,
                max_output_tokens=self.generation.max_output_tokens,
            ),
        )
        text = response.text or ""
        return Answer(
            text=text,
            citations=extract_citations(text, chunks),
            chunks=chunks,
            model=self.generation.model,
        )
