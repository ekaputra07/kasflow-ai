from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from trustcall import create_extractor

from kasflow.llm import medium_llm
from kasflow.utils import read_text_file
from kasflow.db.repository import ExpenseRepository
from kasflow.db.session import sessionmaker
from kasflow.db.models import Expense
from kasflow.graphs.base import BaseGraph
from kasflow.graphs.main.models import MainState

from .models import ExpensesSchema

# create an extractor for ExpensesSchema using medium_llm
_extractor = create_extractor(medium_llm, tools=[ExpensesSchema], tool_choice="ExpensesSchema")


async def extract_node(state: MainState) -> MainState:
    prompt = await read_text_file("graphs/recorder/prompt.md")

    messages = [
        SystemMessage(prompt),
        state.messages[-1],
    ]
    result = await _extractor.ainvoke(messages)

    expenses = []
    for resp in result["responses"]:
        if not isinstance(resp, ExpensesSchema):
            raise ValueError(f"Expected ExpensesSchema, got {type(resp)}")

        for expense in resp.expenses:
            expenses.append(expense.model_dump())

    return {"record_expenses": expenses}


async def store_node(state: MainState) -> MainState:
    expenses = [
        Expense(
            thread_id=state.thread_id,
            user_id=state.user_id,
            amount=expense["amount"],
            category=expense["category"],
            description=expense["description"],
        )
        for expense in state.record_expenses
    ]
    if not expenses:
        return {}
    try:
        async with sessionmaker() as session:
            repo = ExpenseRepository(session)
            await repo.create(expenses)
    except Exception as e:
        return {"record_exception": str(e)}
    return {"record_stored": True}


class RecorderGraph(BaseGraph):
    """
    Recorder graph for extracting expenses from user messages.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(MainState)
        graph.add_node("extract", extract_node)
        graph.add_node("store", store_node)
        graph.add_edge(START, "extract")
        graph.add_edge("extract", "store")
        graph.add_edge("store", END)
        return graph.compile()
