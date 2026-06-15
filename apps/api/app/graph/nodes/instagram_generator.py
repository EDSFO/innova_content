from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def instagram_generator(state: ContentGenerationState) -> dict:
    fallback = {
        "instagram_caption": (
            f"Menos tarefas repetitivas. Mais tempo para decisões. ⚙️\n\n"
            f"• Identifique processos manuais\n• Priorize o que mais consome tempo\n"
            f"• Use IA com regras claras\n• Mantenha revisão humana\n\n"
            f"O objetivo é simples: transformar {state['theme'].lower()} em ganho real de "
            f"produtividade, sem promessas mágicas.\n\n{state['cta']}"
        )
    }
    result = llm.generate_json(
        "instagram_generator",
        "Você escreve legendas B2B diretas para Instagram, com emojis moderados.",
        "Gere JSON com instagram_caption, entre 500 e 1500 caracteres, com gancho, bullets e CTA.\n"
        + context(state),
        fallback,
    )
    return {
        "instagram_caption": result.data["instagram_caption"],
        "logs": append_log(state, result.log),
    }

