from app.graph.content_state import ContentGenerationState
from app.graph.nodes.common import append_log, context
from app.services.llm_service import llm


def youtube_generator(state: ContentGenerationState) -> dict:
    title = f"{state['theme']}: guia prático para empresas"
    scenes = [
        {"time": "0:00 - 0:20", "scene": "Apresentador em plano médio", "voiceover": f"Você ainda perde tempo com {state['theme'].lower()}?", "visual": "Texto-chave na tela"},
        {"time": "0:20 - 0:50", "scene": "Cenas de rotina operacional", "voiceover": "Vamos entender onde está o desperdício.", "visual": "Fluxo manual simplificado"},
        {"time": "0:50 - 2:00", "scene": "Demonstração do problema", "voiceover": state["strategy"]["pain"], "visual": "Lista de impactos"},
        {"time": "2:00 - 3:30", "scene": "Tela com processo automatizado", "voiceover": state["strategy"]["solution"], "visual": "Antes e depois"},
        {"time": "3:30 - 4:30", "scene": "Exemplo prático", "voiceover": "Comece por uma tarefa recorrente, mensurável e de baixo risco.", "visual": "Checklist de implantação"},
        {"time": "4:30 - 5:00", "scene": "Apresentador encerra", "voiceover": state["cta"], "visual": "CTA e marca Innovaapps"},
    ]
    fallback = {
        "youtube_title": title,
        "youtube_description": f"Entenda {state['theme'].lower()} e veja um caminho prático para aplicar essa ideia na sua empresa.\n\n{state['cta']}",
        "youtube_script": "\n\n".join(
            f"{item['time']} | {item['voiceover']}" for item in scenes
        ),
        "video_scenes": scenes,
    }
    result = llm.generate_json(
        "youtube_generator",
        "Você cria roteiros B2B didáticos para vídeos de até cinco minutos.",
        "Gere youtube_title, youtube_description, youtube_script com tempos e video_scenes "
        "(time, scene, voiceover, visual).\n" + context(state),
        fallback,
    )
    return {**result.data, "logs": append_log(state, result.log)}

