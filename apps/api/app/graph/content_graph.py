from langgraph.graph import END, START, StateGraph

from app.graph.content_state import ContentGenerationState
from app.graph.nodes.content_summarizer import content_summarizer
from app.graph.nodes.database_persistor import database_persistor
from app.graph.nodes.hashtag_generator import hashtag_generator
from app.graph.nodes.input_validator import input_validator
from app.graph.nodes.instagram_generator import instagram_generator
from app.graph.nodes.key_points_extractor import key_points_extractor
from app.graph.nodes.linkedin_generator import linkedin_generator
from app.graph.nodes.quality_reviewer import quality_reviewer
from app.graph.nodes.strategy_planner import strategy_planner
from app.graph.nodes.youtube_generator import youtube_generator


def build_content_graph():
    graph = StateGraph(ContentGenerationState)
    nodes = [
        ("input_validator", input_validator),
        ("content_summarizer", content_summarizer),
        ("key_points_extractor", key_points_extractor),
        ("strategy_planner", strategy_planner),
        ("linkedin_generator", linkedin_generator),
        ("instagram_generator", instagram_generator),
        ("youtube_generator", youtube_generator),
        ("hashtag_generator", hashtag_generator),
        ("quality_reviewer", quality_reviewer),
        ("database_persistor", database_persistor),
    ]
    for name, node in nodes:
        graph.add_node(name, node)
    graph.add_edge(START, nodes[0][0])
    for current, following in zip(nodes, nodes[1:], strict=False):
        graph.add_edge(current[0], following[0])
    graph.add_edge(nodes[-1][0], END)
    return graph.compile()


content_graph = build_content_graph()

