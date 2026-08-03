import os
import logging

from langsmith import traceable

from services.ollama_llm_service import call_llm
from coding_harness.states import SubAgentState
from config.env_config import env_settings
from coding_harness.tool_registries.sub_agent_tool_registry import TOOLS as SUB_AGENT_TOOLS
from agentic_tools.adapter import build_ollama_tools

logger = logging.getLogger(__name__)


prompt = f"""
You are a generic helper agent invoked by a master agent.
Your job is to complete whatever task has been delegated to you with the help of avialable tools.
Your tasks:
    - Analyze the task
    - Save the final generate codes or data to files via the CLI
    - You and master agent have access to the same working dir, and all the coding should be done in there
    - Any shell commands executed in this working dir itself; you can read/write files using shell commands
    - Report to the master agent after the task is done with clear description of what has been done

Allowed shell commands are: {env_settings.SHELL_COMMANDS_ALLOWED}
"""

agent_tool_registry = {**SUB_AGENT_TOOLS}
agent_tools = build_ollama_tools(agent_tool_registry)


@traceable
async def generic_sub_agent(state: SubAgentState):
    logger.info("Inside sub agent node")
    os.makedirs(env_settings.AGENT_WORK_DIR, exist_ok=True)

    messages = [{
        "role": "system",
        "content": prompt.strip()
    }]
    messages.extend(state.get("session_messages", []))
    
    llm_response = await call_llm(
        messages=messages,
        model=env_settings.OLLAMA_SUB_AGENT_MODEL,
        tools=agent_tools,
        think=True
    )
    
    state_updates = {
        # "session_messages": []
        "session_messages": state.get("session_messages", [])
    }
    state_updates["agent_calls"] = state.get("agent_calls", 0) + 1
    if llm_response:
        state_updates["session_input_tokens"] = state.get("session_input_tokens", 0) + llm_response.prompt_eval_count
        state_updates["session_output_tokens"] = state.get("session_output_tokens", 0) + llm_response.eval_count
        state_updates["session_current_token_count"] = llm_response.prompt_eval_count + llm_response.eval_count
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

    logger.info("Exiting sub agent node")
    return state_updates