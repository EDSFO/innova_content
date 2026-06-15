from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def linkedin_generator(state: ContentGenerationState) -> dict:
    strategy = state["strategy"]
    fallback = {
        "linkedin_post": (
            f"{state['theme']}\n\n"
            f"Muitas empresas ainda perdem tempo com {strategy['pain'].lower()}.\n\n"
            f"A alternativa não é automatizar tudo sem critério. É {strategy['solution'].lower()}, "
            "começando por processos claros, dados confiáveis e pontos de revisão.\n\n"
            f"Na prática, isso significa mapear uma tarefa recorrente, medir o tempo gasto e "
            f"implementar um agente para apoiar a execução. O resultado esperado é "
            f"{strategy['business_value'].lower()}.\n\n"
            "A tecnologia funciona melhor quando amplia a capacidade da equipe, em vez de "
            "substituir decisões importantes.\n\n"
            f"{state['cta']}"
        )
    }
    result = llm.generate_json(
        "linkedin_generator",
        "Você escreve posts B2B profissionais para LinkedIn, sem promessas exageradas.",
        "Gere JSON com linkedin_post, entre 1200 e 2500 caracteres, com gancho, problema, "
        "solução, exemplo e CTA.\n" + context(state),
        fallback,
    )
    return {"linkedin_post": result.data["linkedin_post"], "logs": append_log(state, result.log)}

