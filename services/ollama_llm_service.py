import logging

from clients.ollama_llm_client import ollama_manager

logger = logging.getLogger(__name__)


async def call_llm(
        messages: list[str],
        model: str,
        think: bool = False,
        tools: list[dict[str, str]] | None = None
):
    logger.debug("Calling llm...")

    llm_response = await ollama_manager.client.chat(
        model=model,
        messages=messages,
        tools=tools,
        think=think
    )

    logger.debug(f"Raw LLM response: {llm_response}")

    return llm_response