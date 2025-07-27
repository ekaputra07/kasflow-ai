from langchain_openai import ChatOpenAI
from kasflow.conf import settings

# llm for light tasks:
# - simple classification
# - basic chat responses
# - quick responses with simple tools/structured outputs
light_llm = ChatOpenAI(
    model="gpt-4.1-nano",
    api_key=settings.openai_api_key,
    temperature=0.0,
    max_tokens=1000,
)

# llm for medium tasks:
# - more complex tools/structured outputs
medium_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=settings.openai_api_key,
    temperature=0.0,
    max_tokens=1000,
)

# llm for heavy/complex tasks
heavy_llm = ChatOpenAI(
    model="gpt-4.1",
    api_key=settings.openai_api_key,
    temperature=0.0,
    max_tokens=1000,
)
