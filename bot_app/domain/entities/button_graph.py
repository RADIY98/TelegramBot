from dataclasses import dataclass
from collections import defaultdict
from typing import List, Dict, DefaultDict


@dataclass
class GraphNode:
    id: int
    title: str


class ButtonsGraph:
    def __init__(self):
        self.nodes: Dict[int, GraphNode] = {}
        self.edges: DefaultDict[int, List[int]] = defaultdict(list)

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node

    def delete_node(self, node: GraphNode) -> None:
        self.nodes.pop(node.id, None)

        self.edges.pop(node.id, None)

        tmpl_edges = self.edges.copy()
        for key, items in tmpl_edges.items():
            self.edges[key] = [item_id for item_id in items if item_id != node.id]

    def connect_nodes(self, parent_node: int, child_id: int) -> None:
        self.edges[parent_node].append(child_id)

    def get_children(self, node_id: int) -> List[int]:
        return self.edges.get(node_id)
