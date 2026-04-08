import networkx as nx

from graphify.profiles import is_balanced_hybrid_graph, node_kind


def test_node_kind_prefers_node_type():
    assert node_kind({"node_type": "actor", "file_type": "document"}) == "actor"


def test_balanced_hybrid_detection_uses_node_types_and_relations():
    G = nx.Graph()
    G.add_node("story_1", label="Budget Vote", file_type="document", node_type="story", story_id="budget-1")
    G.add_node("doc_1", label="Editorial", file_type="document", node_type="document", genre="editorial")
    G.add_node("claim_1", label="Taxes should rise", file_type="document", node_type="claim")
    G.add_edge("doc_1", "story_1", relation="document_in_story", confidence="EXTRACTED")
    G.add_edge("doc_1", "claim_1", relation="quote_expresses_claim", confidence="INFERRED")
    assert is_balanced_hybrid_graph(G) is True


def test_balanced_hybrid_detection_ignores_plain_code_graphs():
    G = nx.Graph()
    G.add_node("n1", label="build", file_type="code", source_file="build.py")
    G.add_node("n2", label="report", file_type="code", source_file="report.py")
    G.add_edge("n1", "n2", relation="calls", confidence="INFERRED")
    assert is_balanced_hybrid_graph(G) is False
