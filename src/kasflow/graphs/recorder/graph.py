from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from trustcall import create_extractor

from kasflow.utils import read_text_file
from kasflow.graphs import BaseGraph
from .models import ExpenseList, RecorderState


_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.0,
    max_tokens=1000,
)
_extractor = create_extractor(
    _llm,
    tools=[ExpenseList],
    tool_choice="ExpenseList",
)


def extract_node(state: RecorderState) -> RecorderState:
    prompt = read_text_file("graphs/recorder/prompt.md")
    messages = [
        SystemMessage(prompt),
        HumanMessage(state.message),
    ]
    result = _extractor.invoke(messages)
    for resp in result["responses"]:
        if not isinstance(resp, ExpenseList):
            raise ValueError(f"Expected ExpenseList, got {type(resp)}")
        return {"expenses": resp.expenses}


class RecorderGraph(BaseGraph):
    """
    Recorder graph for extracting expenses from user messages.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(RecorderState)
        graph.add_node("extract", extract_node)
        graph.add_edge(START, "extract")
        graph.add_edge("extract", END)
        return graph.compile()
