import logging
import asyncio

from coding_harness.states import MainAgentState
from agentic_tools.utils.call_tool import call_function

logger = logging.getLogger(__name__)


async def tool_call(state: MainAgentState):
    logger.info("Calling tool...")
    tasks = []
    tool_registry = state.get("tool_registry", {})
    tool_calls = state.get("tool_calls", [])
    
    for tool_call in tool_calls:
        tasks.append(
            call_function(
                tool_registry=tool_registry,
                fn_name=tool_call["tool_name"],
                fn_args=tool_call["tool_args"]
            )
        )
    
    tool_results = await asyncio.gather(*tasks)
    logger.info(f"Tool results: {tool_results}")
    state["tool_results"] = tool_results
    if tool_results:
        for idx, tool_call in enumerate(tool_calls):
            state["session_messages"].append({
                "role": "tool",
                "tool_name": tool_call["tool_name"],
                "content": tool_results[idx]
            })
    return state
    