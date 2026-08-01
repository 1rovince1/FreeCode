import logging
import asyncio

from coding_harness.states import MainAgentState, SubAgentState
from coding_harness.orchestration_sub_agent import compiled_sub_agent_orchestration

logger = logging.getLogger(__name__)


async def task_dispatcher(state: MainAgentState):
    logger.info("Inside task dispatcher node")
    tool_calls = state.get("tool_calls", [])
    sub_tasks = [
        tool_call["tool_args"]["task"]
        for tool_call in tool_calls
        if tool_call["tool_name"] == "invoke_sub_agent"
    ]

    tasks_to_send = []
    for task in sub_tasks:
        sub_agent_session_messages = [{
            "role": "user",
            "content": f"Your task is: {task}"
        }]
        sub_agent_state: SubAgentState = {
            "current_task": task,
            "session_messages": sub_agent_session_messages
        }
        tasks_to_send.append(
            compiled_sub_agent_orchestration.ainvoke(sub_agent_state)
        )

    sub_agent_results = await asyncio.gather(*tasks_to_send)
    tool_messages = []
    if sub_agent_results:
        for idx, task in enumerate(sub_tasks):
            tool_messages.append({
                "role": "tool",
                "tool_name": "invoke_sub_agent",
                "content": sub_agent_results[idx]["session_messages"][-1]["content"]
            })

    logger.info("Exiting task dispatcher nodes")
    return {
        "session_messages": tool_messages
    }