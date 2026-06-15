from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log
from app.services.llm_service import llm


def key_points_extractor(state: ContentGenerationState) -> dict:
    words = state["summary"].split()
    fallback = {
        "key_points": [
            "Redução de tarefas repetitivas",
            "Mais produtividade para equipes",
            "Aplicação prática com supervisão humana",
        ]
        if len(words) < 12
        else [" ".join(words[i : i + 12]) for i in range(0, min(len(words), 36), 12)]
    }
    result = llm.generate_json(
        "key_points_extractor",
        "Você extrai os pontos mais relevantes de conteúdo empresarial.",
        f"Extraia de três a cinco pontos principais:\n{state['summary']}",
        fallback,
    )
    return {"key_points": result.data["key_points"], "logs": append_log(state, result.log)}

