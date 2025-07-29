from langchain_core.tools import tool
from kasflow.utils import now


@tool
def current_datetime() -> str:
    """
    Returns the current date and time in the format of YYYY-MM-DD HH:MM:SS
    """
    return now().strftime("%Y-%m-%d %H:%M:%S")
