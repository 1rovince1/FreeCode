import logging

from coding_harness.states import MainAgentState, SubAgentState

logger = logging.getLogger(__name__)


def tool_call_decision_edge(state: MainAgentState | SubAgentState) -> str:
    logger.info("Inside tool call decision edge")

    combined_tool_calls = state.get("tool_calls", [])

    # tool_node_tasks = [
    #     tool_call
    #     for tool_call in combined_tool_calls
    #     if tool_call["tool_name"] != "invoke_sub_agent"
    # ]
    # dispatch_node_tasks = [
    #     tool_call
    #     for tool_call in combined_tool_calls
    #     if tool_call["tool_name"] == "invoke_sub_agent"
    # ]
    tool_node_tasks = False
    dispatch_node_tasks = False
    for tool_call in combined_tool_calls:
        if tool_call["tool_name"] == "invoke_sub_agent":
            dispatch_node_tasks = True
        else:
            tool_node_tasks = True
        if dispatch_node_tasks and tool_node_tasks:
            break

    node_list = []
    if tool_node_tasks:
        node_list.append("tool_call")
    if dispatch_node_tasks:
        node_list.append("task_dispatcher")

    return node_list
