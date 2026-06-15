from app.graph.content_state import ContentGenerationState


def database_persistor(state: ContentGenerationState) -> dict:
    return {"persistence_ready": not bool(state.get("errors"))}

