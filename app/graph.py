"""Transaction Relationship Graph Engine using NetworkX
Models entities and surfaces suspicious clusters, shared hardware, and syndicate rings.
"""

from typing import Dict, Any, List
import networkx as nx
from .data import SEED_GRAPH_NODES, SEED_GRAPH_EDGES

class RelationshipGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = SEED_GRAPH_NODES
        self.edges = SEED_GRAPH_EDGES
        self._build()

    def _build(self):
        self.graph.clear()
        for n in self.nodes:
            self.graph.add_node(n["id"], label=n["label"], type=n["type"], risk=n["risk"], detail=n.get("detail", ""))
        for e in self.edges:
            self.graph.add_edge(e["source"], e["target"], relation=e["relation"], alert=e.get("alert", False))

    def analyze_entity(self, user_id: str, device_id: str = None, ip_address: str = None) -> Dict[str, Any]:
        findings = []
        is_syndicate = False
        graph_risk = "LOW"

        # Check for device sharing
        if device_id and device_id in self.graph:
            neighbors = list(self.graph.neighbors(device_id))
            linked_accounts = [n for n in neighbors if self.graph.nodes[n].get("type") == "ACCOUNT"]
            if len(linked_accounts) > 1:
                is_syndicate = True
                graph_risk = "CRITICAL"
                findings.append(f"Syndicate Alert: Hardware device '{device_id}' is shared concurrently across {len(linked_accounts)} distinct accounts ({', '.join(linked_accounts)}). Indicative of an emulator farm.")

        # Check 2-hop compromised paths
        if user_id in self.graph:
            for n in self.graph.neighbors(user_id):
                for hop2 in self.graph.neighbors(n):
                    if hop2 != user_id:
                        edge_data = self.graph.get_edge_data(n, hop2)
                        if edge_data and edge_data.get("alert"):
                            findings.append(f"Compromised Network Path: {user_id} -> {n} -> {hop2} (Relation: {edge_data.get('relation')})")
                            if graph_risk != "CRITICAL":
                                graph_risk = "HIGH"

        if not findings:
            findings.append("No shared hardware fingerprints, proxy collusion, or multi-account mule syndicates detected in 2-hop graph neighborhood.")

        return {
            "entity_id": user_id,
            "device_id": device_id,
            "is_syndicate": is_syndicate,
            "graph_risk": graph_risk,
            "findings": findings
        }

    def get_graph_data(self) -> Dict[str, Any]:
        nodes_list = []
        for n, attrs in self.graph.nodes(data=True):
            nodes_list.append({
                "id": n,
                "label": attrs.get("label", n),
                "type": attrs.get("type", "UNKNOWN"),
                "risk": attrs.get("risk", "LOW"),
                "detail": attrs.get("detail", "Network entity"),
                "degree": self.graph.degree(n)
            })

        edges_list = []
        for u, v, attrs in self.graph.edges(data=True):
            edges_list.append({
                "source": u,
                "target": v,
                "relation": attrs.get("relation", "CONNECTED"),
                "alert": attrs.get("alert", False)
            })

        return {"nodes": nodes_list, "edges": edges_list}

network_graph = RelationshipGraph()

def analyze_graph(user_id: str, device_id: str = None, ip_address: str = None) -> Dict[str, Any]:
    return network_graph.analyze_entity(user_id, device_id, ip_address)

def get_serialized_graph() -> Dict[str, Any]:
    return network_graph.get_graph_data()
