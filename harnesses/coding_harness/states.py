from typing import Literal
from typing_extensions import TypedDict, Annotated


class MainAgentState(TypedDict):
    main_agent_messages: list[dict[str, str]]
    current_user_query: str
    current_conversation_state: Literal["complete", "ongoing"]
    main_agent_calls: int