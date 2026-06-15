from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log
from app.services.llm_service import llm


def content_summarizer(state: ContentGenerationState) -> dict:
    source = state.get("input_text") or state["theme"]
    fallback = {"summary": source[:1200]}
    result = llm.generate_json(
        "content_summarizer",
        "Você resume conteúdo B2B com clareza, sem inventar fatos.",
        f"Resuma em até cinco parágrafos:\n{source}",
        fallback,
    )
    return {"summary": result.data["summary"], "logs": append_log(state, result.log)}

