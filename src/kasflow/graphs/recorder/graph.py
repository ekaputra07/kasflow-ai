from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from trustcall import create_extractor

from kasflow.llm import medium_llm
from kasflow.utils import read_text_file
from kasflow.graphs.base import BaseGraph
from .models import ExpensesSchema, RecorderState

# create an extractor for ExpensesSchema using medium_llm
_extractor = create_extractor(
    medium_llm, tools=[ExpensesSchema], tool_choice="ExpensesSchema"
)


async def extract_node(
    state: RecorderState,
    config: RunnableConfig,
) -> RecorderState:
    user_id = config["configurable"]["user_id"]
    prompt = await read_text_file("graphs/recorder/prompt.md")

    messages = [
        SystemMessage(prompt),
        HumanMessage(state.message),
    ]
    result = await _extractor.ainvoke(messages)

    for resp in result["responses"]:
        if not isinstance(resp, ExpensesSchema):
            raise ValueError(f"Expected ExpensesSchema, got {type(resp)}")

        # assign user_id to each expense
        for expense in resp.expenses:
            expense.user_id = user_id
        return {"record_expenses": resp.expenses}


async def store_node(
    state: RecorderState, config: RunnableConfig
) -> RecorderState:
    expenses = state.record_expenses
    if not expenses:
        return {}
    try:
        store = config["configurable"]["store"]
        await store.create_expense(expenses)
    except Exception as e:
        return {"record_exception": str(e)}
    return {"record_stored": True}


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
