from langchain_core.messages import SystemMessage
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately,
)
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from kasflow.conf import settings
from kasflow.llm import medium_llm
from kasflow.utils import read_text_file
from kasflow.graphs.base import BaseGraph
from kasflow.graphs.main.models import MainState
from kasflow.tools import all_tools

_llm_with_tools = medium_llm.bind_tools(all_tools)


async def chat_node(state: MainState) -> MainState:
    prompt = await read_text_file("graphs/chat/prompt.md")
    messages = [
        SystemMessage(
            prompt.format(
                bot_name=settings.bot_name,
            )
        )
    ] + state.messages

    messages = trim_messages(
        messages,
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=1000,
        start_on="human",
        include_system=True,
    )
    response = await _llm_with_tools.ainvoke(messages)
    return {"chat_response": response.content, "messages": [response]}


class ChatGraph(BaseGraph):
    """
    Chat graph for handling user messages and generating responses.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(MainState)

        # nodes
        graph.add_node("chat", chat_node)
        graph.add_node("tools", ToolNode(tools=all_tools))

        # edges
        graph.add_edge(START, "chat")
        graph.add_conditional_edges("chat", tools_condition)
        graph.add_edge("tools", "chat")
        graph.add_edge("chat", END)
        return graph.compile()
