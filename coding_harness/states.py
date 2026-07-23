from typing_extensions import TypedDict


class MainAgentState(TypedDict):
    session_messages: list[dict[str, str]]
    main_agent_calls: int
    session_input_tokens: int
    session_output_tokens: int
    tool_registry: dict
    tool_calls: list
    tool_results: list