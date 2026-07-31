from langgraph.types import Send

from coding_harness.states import MainAgentState, SubAgentState


async def task_dispatcher(state: MainAgentState):
    list_tasks = state.get("tool_calls", [])

    tasks_to_send = []
    for task in list_tasks:
        sub_agent_state = SubAgentState.copy()
        sub_agent_state["current_task"] = task
        tasks_to_send.append(
            Send(
                "sub_agent",
                sub_agent_state
            )
        )

    return tasks_to_send