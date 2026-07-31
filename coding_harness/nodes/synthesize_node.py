from coding_harness.states import MainAgentState


async def task_synthesizer(state: MainAgentState):
    sub_agent_task_results = state.get("sub_agent_results", [])

    sub_agent_result_messages = []
    for result in sub_agent_task_results:
        sub_agent_result_messages.append({
            "role": "tool",
            "tool_name": "invoke_sub_agent",
            "content": result
        })

    return {
        "session_messages": state["session_messages"] + sub_agent_result_messages
    }