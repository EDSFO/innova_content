from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def quality_reviewer(state: ContentGenerationState) -> dict:
    fallback = {
        "quality_score": 8,
        "review_notes": [
            "Conteúdo coerente com o tema e público",
            "CTA presente",
            "Revisão humana recomendada antes da publicação",
        ],
    }
    result = llm.generate_json(
        "quality_reviewer",
        "Você revisa clareza, coerência, adequação ao canal e promessas exageradas.",
        "Avalie de 0 a 10 e retorne quality_score e review_notes.\n" + context(state),
        fallback,
    )
    return {**result.data, "logs": append_log(state, result.log)}

