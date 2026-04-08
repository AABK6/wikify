"""Domain profiles for mixed-corpus graphify workflows."""
from __future__ import annotations

import networkx as nx


BALANCED_HYBRID_NODE_TYPES = frozenset({
    "story",
    "document",
    "actor",
    "claim",
    "topic",
    "event",
    "stance",
    "perspective",
    "quote",
    "span",
})

BALANCED_HYBRID_EDGE_TYPES = frozenset({
    "document_in_story",
    "document_mentions_topic",
    "document_describes_event",
    "document_has_perspective",
    "quote_in_document",
    "quote_by_actor",
    "quote_expresses_claim",
    "span_supports_claim",
    "actor_makes_claim",
    "claim_about_topic",
    "claim_about_event",
    "actor_takes_stance",
    "stance_toward_claim",
    "stance_toward_actor",
    "perspective_groups_claim",
    "claim_supports_claim",
    "claim_conflicts_with_claim",
    "event_precedes_event",
})

BALANCED_HYBRID_METADATA_FIELDS = frozenset({
    "outlet",
    "genre",
    "story_id",
    "published_at",
    "author",
    "source_url",
})


def _normalise(value: object) -> str:
    return str(value).strip().lower() if value not in (None, "") else ""


def node_kind(data: dict) -> str:
    """Preferred semantic kind for a node, falling back to file_type."""
    return _normalise(data.get("node_type")) or _normalise(data.get("file_type"))


def is_balanced_hybrid_graph(G: nx.Graph) -> bool:
    """Heuristic: does this graph look like a discourse/news corpus?"""
    node_types = {node_kind(data) for _, data in G.nodes(data=True)} - {""}
    relation_types = {
        _normalise(data.get("relation"))
        for _, _, data in G.edges(data=True)
        if data.get("relation")
    }
    has_metadata = any(
        any(_normalise(data.get(field)) for field in BALANCED_HYBRID_METADATA_FIELDS)
        for _, data in G.nodes(data=True)
    )

    discourse_node_hits = len(node_types & BALANCED_HYBRID_NODE_TYPES)
    discourse_relation_hits = len(relation_types & BALANCED_HYBRID_EDGE_TYPES)

    if discourse_node_hits >= 2:
        return True
    if discourse_relation_hits >= 2 and (has_metadata or discourse_node_hits >= 1):
        return True
    if discourse_node_hits >= 1 and discourse_relation_hits >= 1:
        return True
    return False
