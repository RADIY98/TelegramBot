from ..domain.entities.button_graph import ButtonsGraph


class GraphManager:
    def __init__(self, graph: ButtonsGraph):
        self.graph = graph

    def set_start_graph(self):
        self._set_welcome_buttons()


    def _set_welcome_buttons(self):
        self.graph.add_nodes()