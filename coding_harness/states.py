from typing import Annotated
from typing_extensions import TypedDict
import operator


class MainAgentState(TypedDict):
    session_messages: Annotated[list[dict[str, str]], operator.add]
    main_agent_calls: int
    session_input_tokens: int
    session_output_tokens: int
    tool_registry: dict
    tool_calls: list
    tool_results: list
    # sub_agent_calls: list
    # sub_agent_results: Annotated[list[str], operator.add]

class SubAgentState(TypedDict):
    # tasks: list[str]
    # tasks_results: Annotated[list[str], operator.add]
    current_task: str
    session_messages: Annotated[list[dict[str, str]], operator.add]
    sub_agent_calls: int
    session_input_tokens: int
    session_output_tokens: int
    tool_registry: dict
    tool_calls: list
    tool_results: list