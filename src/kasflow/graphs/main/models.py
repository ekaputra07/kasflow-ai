from typing import Literal, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class IntentionSchema(BaseModel):
    intention: Literal["chat", "record"] = Field(description="Intention detected from user message")


class MainState(BaseModel):
    # -- accessible in all nodes
    messages: Annotated[list[AnyMessage], add_messages] = Field(
        description="List of messages in the conversation",
        default_factory=list,
    )
    thread_id: int = Field(
        description="Thread ID of the conversation",
    )
    user_id: int = Field(
        description="User ID of the user",
    )

    # -- set by the intention node
    intention: Literal["chat", "record"] = Field(
        description="Intention detected from user message",
        default="chat",
    )

    # -- set by the chat graph
    chat_response: str = Field(description="Response generated by the chat assistant", default="")

    # -- set by the recorder graph
    record_expenses: list[dict] = Field(
        description="A list of expense records", default_factory=list
    )
    record_stored: bool = Field(
        description="Indicates if the expense record was successfully stored",
        default=False,
    )
    record_exception: str = Field(
        description=("Exception message if there was an error storing the expense record"),
        default="",
    )
