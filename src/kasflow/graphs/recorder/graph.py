from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from trustcall import create_extractor

from kasflow.conf import settings
from kasflow.utils import read_text_file
from kasflow.graphs.base import BaseGraph
from .models import ExpenseList, RecorderState


_llm = ChatOpenAI(model="gpt-4.1-mini", api_key=settings.openai_api_key, temperature=0.0, max_tokens=1000)
_extractor = create_extractor(_llm, tools=[ExpenseList], tool_choice="ExpenseList")


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


def store_node(state: RecorderState, config: RunnableConfig) -> RecorderState:
    expenses = state.expenses
    if not expenses:
        return {}
    try:
        store = config["configurable"]["store"]
        store.create_expense(expenses)
    except Exception as e:
        return {"store_exception": str(e)}
    return {"stored": True}


class RecorderGraph(BaseGraph):
    """
    Recorder graph for extracting expenses from user messages.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(RecorderState)
        graph.add_node("extract", extract_node)
        graph.add_node("store", store_node)
        graph.add_edge(START, "extract")
        graph.add_edge("extract", "store")
        graph.add_edge("store", END)
        return graph.compile()
