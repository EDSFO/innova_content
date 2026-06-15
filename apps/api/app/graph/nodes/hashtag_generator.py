from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def hashtag_generator(state: ContentGenerationState) -> dict:
    fallback = {
        "hashtags": [
            "#inteligenciaartificial",
            "#automacao",
            "#produtividade",
            "#negocios",
            "#transformacaodigital",
        ]
    }
    result = llm.generate_json(
        "hashtag_generator",
        "Você seleciona hashtags relevantes e específicas para conteúdo B2B.",
        "Gere JSON com cinco a oito hashtags, sem duplicatas.\n" + context(state),
        fallback,
    )
    return {"hashtags": result.data["hashtags"], "logs": append_log(state, result.log)}

