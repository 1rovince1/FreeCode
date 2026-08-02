import os
import logging

from langsmith import traceable

from services.ollama_llm_service import call_llm
from coding_harness.states import MainAgentState
from config.env_config import env_settings
from coding_harness.tool_registries.main_agent_tool_registry import TOOLS as MAIN_AGENT_TOOLS
from agentic_tools.adapter import build_ollama_tools

logger = logging.getLogger(__name__)


prompt = """
You are a coding assistant.
You have access to a few tools to help with your job.
Your tasks:
    - Analyze the user request
    - Ask to the user for any clarifications requried to perform the given task
    - If the task is of less complexity, do it on your own
    - If the task is complex you can delegate tasks to sub agents with detailed instructions on what to do, file paths etc.
    - If nature of tasks allows it, then multiple sub agents should be used in parallel to keep individual workload in check
    - Task given to a sub agent should be simple and complete instructions should be provided for guidance
    - You and sub agents have access to the same working dir, and all the coding should be done in there
    - Any shell commands executed in this working dir itself; you can read/write files using shell commands
    - Consolidate the final reply to the user after the task is done
"""

agent_tool_registry = {**MAIN_AGENT_TOOLS}
agent_tools = build_ollama_tools(agent_tool_registry)


@traceable
async def main_agent(state: MainAgentState):
    logger.info("Inside main agent node")
    logger.debug(f"state inside main agent node: {state}")
    os.makedirs(env_settings.AGENT_WORK_DIR, exist_ok=True)

    messages = [{
        "role": "system",
        "content": prompt.strip()
    }]
    messages.extend(state.get("session_messages", []))
    
    llm_response = await call_llm(
        messages=messages,
        model=env_settings.OLLAMA_MAIN_AGENT_MODEL,
        tools=agent_tools,
        think=True
    )

    state_updates = {
        "session_messages": []
    }
    state_updates["main_agent_calls"] = state.get("main_agent_calls", 0) + 1
    if llm_response:
        state_updates["session_input_tokens"] = state.get("session_input_tokens", 0) + llm_response.prompt_eval_count
        state_updates["session_output_tokens"] = state.get("session_output_tokens", 0) + llm_response.eval_count
    if llm_response.message.content:
        state_updates["session_messages"].append({
            "role": "assistant",
            "content": llm_response.message.content
        })
    if llm_response.message.tool_calls:
        state_updates["tool_registry"] = agent_tool_registry
        state_updates["tool_calls"] = [
            {
                "tool_name": tool_call.function.name,
                "tool_args": tool_call.function.arguments
            } for tool_call in llm_response.message.tool_calls
        ]
        state_updates["session_messages"].append({
            "role": "assistant",
            "tool_calls": [tool_call.model_dump() for tool_call in llm_response.message.tool_calls]
        })
    else:
        state_updates["tool_registry"] = {}
        state_updates["tool_calls"] = []
        state_updates["tool_results"] = []

    logger.info("Exiting main agent node")
    return state_updates