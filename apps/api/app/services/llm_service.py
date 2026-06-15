import json
import time
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from app.config.settings import get_settings


@dataclass
class LLMResult:
    data: Any
    log: dict


class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.client = (
            OpenAI(api_key=self.settings.openai_api_key)
            if self.settings.llm_provider == "openai" and self.settings.openai_api_key
            else None
        )

    def generate_json(self, node: str, instructions: str, prompt: str, fallback: Any) -> LLMResult:
        if not self.client:
            return LLMResult(
                fallback,
                self._log(node, 0, "success", prompt_tokens=0, completion_tokens=0),
            )
        started = time.perf_counter()
        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                instructions=instructions,
                input=prompt + "\nRetorne somente JSON válido.",
                text={"format": {"type": "json_object"}},
                store=False,
            )
            data = json.loads(response.output_text)
            if not self._matches_shape(data, fallback):
                return LLMResult(
                    fallback,
                    self._log(
                        node,
                        int((time.perf_counter() - started) * 1000),
                        "fallback",
                        error="A resposta da LLM não corresponde ao contrato esperado",
                    ),
                )
            usage = response.usage
            return LLMResult(
                data,
                self._log(
                    node,
                    int((time.perf_counter() - started) * 1000),
                    "success",
                    getattr(usage, "input_tokens", None),
                    getattr(usage, "output_tokens", None),
                ),
            )
        except Exception as exc:
            return LLMResult(
                fallback,
                self._log(node, int((time.perf_counter() - started) * 1000), "fallback", error=str(exc)),
            )

    def _matches_shape(self, data: Any, expected: Any) -> bool:
        if isinstance(expected, dict):
            if not isinstance(data, dict) or not all(key in data for key in expected):
                return False
            return all(self._matches_shape(data[key], value) for key, value in expected.items())
        if isinstance(expected, list):
            return isinstance(data, list)
        return isinstance(data, type(expected))

    def _log(
        self,
        node: str,
        latency_ms: int,
        status: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        error: str | None = None,
    ) -> dict:
        return {
            "node_name": node,
            "provider": self.settings.llm_provider,
            "model": self.settings.openai_model if self.client else "mock-v1",
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": (
                prompt_tokens + completion_tokens
                if prompt_tokens is not None and completion_tokens is not None
                else None
            ),
            "latency_ms": latency_ms,
            "status": status,
            "error_message": error,
        }


llm = LLMService()
