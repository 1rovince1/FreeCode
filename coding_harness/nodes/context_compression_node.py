import logging

from services.ollama_llm_service import call_llm
from coding_harness.states import MainAgentState, SubAgentState
from config.env_config import env_settings

logger = logging.getLogger(__name__)


prompt = """
You are a context compression agent.
Your job is to compress the given context into a brief summary.
The context will be brief, but it should contain eveything that has happened till now,
and what is currently requested by the user, or what is being done at the moment should be preserved
as it is of great importance.
"""

async def context_compressor(state: MainAgentState | SubAgentState):
    logger.info("Inside context compression node")
    messages_to_compress = state.get("session_messages", [])
    messages = [
        {
            "role": "system",
            "content": prompt.strip()
        },
        {
            "role": "user",
            "conent": f"Context to compress:\n{messages_to_compress}"
        }
    ]
    llm_response = await call_llm(
        messages=messages,
        model=env_settings.OLLAMA_CONTEXT_COMPRESSION_MODEL
    )

    updated_session_messages = [{
        "role": "user",
        "content": f"Compressed context of what happened till now:\n{llm_response.message.content}"
    }]

    logger.info("Exiting context compression node")
    return {
        "session_messages": updated_session_messages
    }