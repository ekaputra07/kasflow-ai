from datetime import datetime
from langchain_core.tools import tool


@tool
def current_datetime() -> str:
    """
    Returns the current date and time in the format of YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
