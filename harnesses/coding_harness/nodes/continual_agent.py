from langsmith import traceable

from services.ollama_llm_service import call_llm
from harnesses.coding_harness.states import MainAgentState


prompt = """
Based on the given conversation history, calssify whether the conversation is ongoing, or the task is complete.
Return only one work in the response:
    - complete
    - ongoing
Do not give any explanation, just give the response as one word.
"""

@traceable
async def continual_agent(state: MainAgentState):
    messages = [{
        "role": "system",
        "content": prompt
    }]
    messages.extend(state.get("main_agent_messages", []))

    response = await call_llm(
        messages=messages,
        model="gemma4:cloud"
    )

    state["current_conversation_state"] = response.message.content
    return state


async def continue_or_not(state: MainAgentState):
    return state.get("current_conversation_state", "ongoing")