from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from kasflow.conf import settings
from kasflow.utils import read_text_file
from kasflow.graphs.base import BaseGraph
from kasflow.graphs.recorder import RecorderGraph
from kasflow.graphs.chat import ChatGraph

from .models import IntentionSchema, MainState

recorder = RecorderGraph().compiled
chat = ChatGraph().compiled

_llm = ChatOpenAI(
    model="gpt-4.1-nano",
    api_key=settings.openai_api_key,
    temperature=0.0,
    max_tokens=1000,
).with_structured_output(IntentionSchema)


async def intention_node(
    state: MainState,
    config: RunnableConfig,
) -> MainState:
    prompt = await read_text_file("graphs/main/prompt.md")
    messages = [
        SystemMessage(prompt),
        HumanMessage(state.message),
    ]
    response = await _llm.ainvoke(messages)
    return {"intention": response.intention}


def intent_conditions(state: MainState) -> str:
    """
    Route to the appropriate subgraph based on the detected intention.
    """
    if state.intention == "record":
        return "record"
    else:
        return "chat"  # Default to chat if intention is unknown


class MainGraph(BaseGraph):
    """
    Main graph for routing subgraphs based on user intention.
    It detects the user's intention (chat or record) and routes to the appropriate subgraph.
    """

    def compile(self) -> StateGraph:
        graph = StateGraph(MainState)
        graph.add_node("intention", intention_node)
        graph.add_node("chat", chat)
        graph.add_node("record", recorder)

        graph.add_edge(START, "intention")
        graph.add_conditional_edges(
            "intention", intent_conditions, ["chat", "record"]
        )
        graph.add_edge(["chat", "record"], END)
        return graph.compile()
