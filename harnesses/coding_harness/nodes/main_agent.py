import os

from deepagents import create_deep_agent, FilesystemPermission
from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend
from langsmith import traceable

from services.ollama_llm_service import call_llm
from harnesses.coding_harness.states import MainAgentState


prompt = """
You are a coding assistant.
Your tasks:
    - Analyze the user request
    - Ask to the user for any clarifications requried to perform the given task
    - If the task is of less complexity, do it on your own
    - If the task is complex, create a to do list, and then delegate task to agents via task tool
    - Save the final generate codes or data to files via the file tools
    - if given a coding task, write proper test cases to check each functionality thoroughly
    - Consolidate the final reply to the user after the task is done
"""

@traceable
async def main_agent(state: MainAgentState):
    os.makedirs("../../../playground", exist_ok=True)

    messages = [{
        "role": "system",
        "content": prompt
    }]
    messages.extend(state.get("main_agent_messages", []))
    # print(state)
    # await call_llm(
    #     messages=messages,
    #     model="gemma4:cloud",
    #     tools=
    # )


    agent = create_deep_agent(
        # model="ollama:gemma4:cloud",
        model="ollama:gpt-oss:120b-cloud",
        system_prompt=prompt,
        backend=FilesystemBackend(
            root_dir="/home/unthinkable-lap/Desktop/practice/code_agent_harness/playground",
            virtual_mode=True
        ),
        # backend=CompositeBackend(
        #     default=StateBackend(),
        #     routes={
        #         "/workspace": FilesystemBackend(
        #             root_dir="/home/unthinkable-lap/Desktop/practice/code_agent_harness/playground",
        #             virtual_mode=True
        #         )
        #     }
        # ),
        permissions=[
            FilesystemPermission(
                operations=["read", "write"],
                paths=["/home/unthinkable-lap/Desktop/practice/code_agent_harness/playground/**"],
                mode="allow"
            )
        ]
    )

    # print(await agent.ainvoke({
    #     "messages": messages
    # }))

    response = await agent.ainvoke({
        "messages": messages
    })
    # print(response)

    state["main_agent_calls"] = state.get("main_agent_calls", 0) + 1
    state["main_agent_messages"].append({
        "role": "assistant",
        "content": response["messages"][-1].content
    })
    return state