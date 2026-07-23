from typing import Literal
from typing_extensions import TypedDict, Annotated


class MainAgentState(TypedDict):
    session_messages: list[dict[str, str]]
    current_user_query: str
    current_conversation_state: Literal["complete", "ongoing"]
    main_agent_calls: int
    tool_registry: dict
    tool_calls: list
    tool_results: list