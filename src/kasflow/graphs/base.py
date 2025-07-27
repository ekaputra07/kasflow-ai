from abc import ABC, abstractmethod
from langgraph.graph import StateGraph


class BaseGraph(ABC):
    """
    Abstract base class for all graph types.
    """

    _compiled_graph: StateGraph | None = None

    @abstractmethod
    def compile(self) -> StateGraph:
        """
        Respond to a greeting.
        """
        pass

    @property
    def compiled(self) -> StateGraph:
        """
        Get the compiled state graph.
        """
        if self._compiled_graph:
            return self._compiled_graph
        self._compiled_graph = self.compile()
        return self._compiled_graph

    def draw(self, xray: int = 0) -> None:
        """
        Draw the graph in Mermaid format.
        """
        return self.compiled.get_graph(xray=xray).draw_mermaid_png()
