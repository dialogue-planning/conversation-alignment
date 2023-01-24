from typing import Iterable, Dict
from graphviz import Digraph


class GraphGenerator:
    """Builds a basic graph with graphviz."""
    def __init__(self):
        self._idx = "0"
        self._parent = "0"
        self.graph = Digraph(strict=True)
        self.graph.node(
            self._idx,
            "START",
            fillcolor="darkolivegreen3",
            style="filled",
            fontsize="50",
        )

    def _inc_idx(self, inc: int = 1):
        self._idx = str(int(self._idx) + inc)

    def _set_last_chosen(self, new_id):
        self._parent = str(new_id)

    def complete_conversation(self, final_val):
        self.create_from_parent(
            {"GOAL REACHED": final_val}, "darkolivegreen3", "GOAL REACHED"
        )

    def create_from_parent(
        self, nodes: Dict[str, float], fillcolor: str, new_parent: str = None
    ):
        for node, conf in nodes.items():
            edge_color, penwidth = "grey45", "5.0"
            self._inc_idx()
            self.graph.node(
                self._idx,
                f"{node}\n{conf}",
                fillcolor=fillcolor,
                style="filled",
                fontsize="50",
            )
            if new_parent:
                if node == new_parent:
                    new_parent_id = self._idx
                    edge_color, penwidth = "forestgreen", "10.0"
            self.graph.edge(
                self._parent, self._idx, color=edge_color, penwidth=penwidth
            )
        if new_parent:
            self._set_last_chosen(new_parent_id)


class BeamSearchGraphGenerator(GraphGenerator):
    """Handles building a graph for beam search.

    Args
        k (int): The k value for the beam search.
    """
    class GraphBeam:
        """Inner class that holds the id maps for each beam so that any node
        can be easily referenced.
        """
        def __init__(self, parent_nodes_id_map: Dict = None):
            if not parent_nodes_id_map:
                parent_nodes_id_map = {"START": ["0"]}
            self.parent_nodes_id_map = {
                name: [idx for idx in ids] for name, ids in parent_nodes_id_map.items()
            }

    def __init__(self, k: int):
        super().__init__()
        self.beams = [self.GraphBeam() for _ in range(k)]

    def set_last_chosen(self, node: str, beam: int):
        self._set_last_chosen(self.beams[beam].parent_nodes_id_map[node][-1])

    def create_nodes_highlight_k(
        self,
        nodes: Dict[str, float],
        fillcolor: str,
        parent: str,
        beam: int,
        k_chosen: Iterable[str],
    ):
        # have to access the parent ID before potentially making changes to the map to prevent
        # overwriting in the case where you have a node "A" connected to a parent "A"
        # (otherwise you would attach the node to itself)
        parent = self.beams[beam].parent_nodes_id_map[parent][-1]
        for node, conf in nodes.items():
            edge_color, arrowhead, penwidth = "grey45", "none", "5.0"
            self._inc_idx()
            self.graph.node(
                self._idx,
                f"{node}\n{conf}",
                fillcolor=fillcolor,
                style="filled",
                fontsize="50",
            )

            if node in k_chosen:
                edge_color, arrowhead, penwidth = "purple", "normal", "10.0"
                # create the list if it doesn't exist yet, otherwise add to it
                if node not in self.beams[beam].parent_nodes_id_map:
                    self.beams[beam].parent_nodes_id_map[node] = []
                self.beams[beam].parent_nodes_id_map[node].append(self._idx)

            self.graph.edge(
                parent,
                self._idx,
                color=edge_color,
                penwidth=penwidth,
                arrowhead=arrowhead,
            )
