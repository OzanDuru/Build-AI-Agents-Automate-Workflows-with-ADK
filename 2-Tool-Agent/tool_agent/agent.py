from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    now = datetime.now()
    return {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "current_date": now.strftime("%Y-%m-%d"),
        "timestamp": now.timestamp(),
    }

root_agent = Agent(
    name="greeting_agent",
    model = "gemini-2.0-flash",
    description="Tool Agent.",
    instruction="""
    You are a helpful assistant that can use the following tools:
    1. get_current_time: Get the current time in various formats.
    """,
     tools=[get_current_time]
    # tools =[google_search]
)