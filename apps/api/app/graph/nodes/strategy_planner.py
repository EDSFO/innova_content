from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def strategy_planner(state: ContentGenerationState) -> dict:
    fallback = {
        "strategy": {
            "main_angle": state["theme"],
            "pain": "Tempo perdido em tarefas repetitivas e produção inconsistente",
            "solution": "Aplicar inteligência artificial com processo e revisão humana",
            "business_value": "Ganhar produtividade e consistência comercial",
            "cta": state["cta"],
            "content_pillar": "Inteligência artificial aplicada aos negócios",
        }
    }
    result = llm.generate_json(
        "strategy_planner",
        "Você é estrategista de conteúdo B2B de tecnologia e automação.",
        "Crie estratégia com main_angle, pain, solution, business_value, cta e content_pillar.\n"
        + context(state),
        fallback,
    )
    return {"strategy": result.data["strategy"], "logs": append_log(state, result.log)}

