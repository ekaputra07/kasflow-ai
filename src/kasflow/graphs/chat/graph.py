from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from kasflow.conf import settings
from kasflow.utils import read_text_file, format_currency
from kasflow.graphs.base import BaseGraph
from .models import ChatState

_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=settings.openai_api_key,
    temperature=0.0,
    max_tokens=1000,
)


async def chat_node(
    state: ChatState,
    config: RunnableConfig,
) -> ChatState:
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

    messages = [
        SystemMessage(
            prompt.format(
                bot_name=settings.bot_name, expenses=formatted_expenses
            )
        ),
        HumanMessage(state.message),
    ]
    response = await _llm.ainvoke(messages)
    return {"chat_response": response.content}


class ChatGraph(BaseGraph):
    """
    Chat graph for handling user messages and generating responses.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(ChatState)
        graph.add_node("chat", chat_node)
        graph.add_edge(START, "chat")
        graph.add_edge("chat", END)
        return graph.compile()
