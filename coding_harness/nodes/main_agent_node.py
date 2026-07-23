import os
from pprint import pprint

from deepagents import create_deep_agent, FilesystemPermission
from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend
from langsmith import traceable

from services.ollama_llm_service import call_llm
from coding_harness.states import MainAgentState
from config.env_config import env_settings
from agentic_tools.tool_registry import TOOLS as MAIN_AGENT_TOOLS
from agentic_tools.adapter import build_ollama_tools


prompt = """
You are a coding assistant.
Your tasks:
    - Analyze the user request
    - Ask to the user for any clarifications requried to perform the given task
    - If the task is of less complexity, do it on your own
    - If the task is complex, create a to do list, and then you can delegate tasks to other agents using the task tool repetitively
    - Save the final generate codes or data to files via the file tools
    - if given a coding task, write proper test cases to check each functionality thoroughly
    - Consolidate the final reply to the user after the task is done
"""

# @traceable
# async def main_agent(state: MainAgentState):
#     os.makedirs(env_settings.AGENT_WORK_DIR, exist_ok=True)

#     # messages = [{
#     #     "role": "system",
#     #     "content": prompt
#     # }]
#     # messages.extend(state.get("main_agent_messages", []))
#     # print(state)
#     # await call_llm(
#     #     messages=messages,
#     #     model="gemma4:cloud",
#     #     tools=
#     # )


#     agent = create_deep_agent(
#         model=env_settings.OLLAMA_MAIN_AGENT_MODEL,
#         system_prompt=prompt,
#         backend=FilesystemBackend(
#             root_dir=env_settings.AGENT_WORK_DIR,
#             virtual_mode=True
#         ),
#         # backend=CompositeBackend(
#         #     default=StateBackend(),
#         #     routes={
#         #         "/workspace": FilesystemBackend(
#         #             root_dir="/home/unthinkable-lap/Desktop/practice/code_agent_harness/playground",
#         #             virtual_mode=True
#         #         )
#         #     }
#         # ),
#         permissions=[
#             FilesystemPermission(
#                 operations=["read", "write"],
#                 paths=[os.path.join(env_settings.AGENT_WORK_DIR, "**")],
#                 mode="allow"
#             )
#         ]
#     )

#     # print(await agent.ainvoke({
#     #     "messages": messages
#     # }))

#     response = await agent.ainvoke({
#         # "messages": messages
#         "messages": state.get("session_messages", [])
#     })
#     # print(response)
#     # with open("response.txt", "w") as file:
#     #     pprint(response, stream=file)

#     state["main_agent_calls"] = state.get("main_agent_calls", 0) + 1
#     state["session_messages"].append({
#         "role": "assistant",
#         "content": response["messages"][-1].content
#     })
#     # with open("response_session_messages.txt", "w") as file:
#     #     pprint(state["session_messages"], stream=file)

#     return state


main_agent_tool_registry = {**MAIN_AGENT_TOOLS}
main_agent_tools = build_ollama_tools(main_agent_tool_registry)
print(main_agent_tools)

@traceable
async def main_agent(state: MainAgentState):
    os.makedirs(env_settings.AGENT_WORK_DIR, exist_ok=True)

    messages = [{
        "role": "system",
        "content": prompt.strip()
    }]
    messages.extend(state.get("session_messages", []))
    
    # print(state)
    llm_response = await call_llm(
        messages=messages,
        model=env_settings.OLLAMA_MAIN_AGENT_MODEL,
        tools=main_agent_tools
    )
    
    # state["tool_calls"] = llm_response.message.tool_calls
    state["tool_calls"] = [{"tool_name": tool_call.function.name, "tool_args": tool_call.function.arguments} for tool_call in llm_response.message.tool_calls]
    state["tool_registry"] = main_agent_tool_registry
    state["main_agent_calls"] = state.get("main_agent_calls", 0) + 1
    if llm_response.message.content:
        state["session_messages"].append({
            "role": "assistant",
            "content": llm_response.message.content
        })
    
    return state