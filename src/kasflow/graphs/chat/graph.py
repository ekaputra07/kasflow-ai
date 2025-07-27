from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately,
)
from langgraph.graph import StateGraph, START, END

from kasflow.conf import settings
from kasflow.llm import medium_llm
from kasflow.utils import read_text_file, format_currency
from kasflow.graphs.base import BaseGraph
from kasflow.graphs.main.models import MainState


async def chat_node(
    state: MainState,
    config: RunnableConfig,
) -> MainState:
    prompt = await read_text_file("graphs/chat/prompt.md")

    store = config["configurable"]["store"]
    expenses = await store.list_expenses()
    formatted_expenses = (
        "\n".join(
            [
                f"{e.created.strftime('%b %d %H:%M')} - {format_currency(e.amount)} - {e.description}"
                for e in expenses
            ]
        )
        if expenses
        else "No expenses found."
    )

    messages = trim_messages(
        state.messages,
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=128,
        start_on="human",
        end_on=("human", "tool"),
    )

    messages = [
        SystemMessage(
            prompt.format(
                bot_name=settings.bot_name,
                expenses=formatted_expenses,
            )
        )
    ] + messages
    response = await medium_llm.ainvoke(messages)
    return {"chat_response": response.content, "messages": [response]}


class ChatGraph(BaseGraph):
    """
    Chat graph for handling user messages and generating responses.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(MainState)
        graph.add_node("chat", chat_node)
        graph.add_edge(START, "chat")
        graph.add_edge("chat", END)
        return graph.compile()
