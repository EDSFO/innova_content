from app.graph.content_state import ContentGenerationState


def input_validator(state: ContentGenerationState) -> dict:
    if not (state.get("theme") or state.get("input_text")):
        return {"errors": ["Tema ou texto de entrada é obrigatório"]}
    return {
        "audience": state.get("audience") or "empresários e gestores",
        "objective": state.get("objective") or "gerar autoridade",
        "tone": state.get("tone") or "consultivo",
        "cta": state.get("cta") or "Converse com a Innovaapps",
        "errors": [],
        "logs": [],
    }

