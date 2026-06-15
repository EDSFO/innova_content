from app.graph.content_state import ContentGenerationState


def context(state: ContentGenerationState) -> str:
    source = state.get("input_text") or state["theme"]
    return (
        f"Tema: {state['theme']}\nConteúdo: {source}\nPúblico: {state['audience']}\n"
        f"Objetivo: {state['objective']}\nTom: {state['tone']}\nCTA: {state['cta']}\n"
        f"Resumo: {state.get('summary', '')}\nPontos: {state.get('key_points', [])}\n"
        f"Estratégia: {state.get('strategy', {})}"
    )


def append_log(state: ContentGenerationState, log: dict) -> list[dict]:
    return [*state.get("logs", []), log]

