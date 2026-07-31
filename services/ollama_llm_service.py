import logging

from ollama import ChatResponse

from clients.ollama_llm_client import ollama_manager
# from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)


async def call_llm(
        messages: list[str],
        model: str,
        think: bool = False,
        tools: list[dict[str, str]] | None = None
) -> ChatResponse:
    logger.info("Calling llm...")

    llm_response = await ollama_manager.client.chat(
        model=model,
        messages=messages,
        tools=tools,
        think=think
    )

    logger.info(f"Raw LLM response: {llm_response}")
    logger.info(f"Token usage:\nInput tokens: {llm_response.prompt_eval_count}\nOutput tokens: {llm_response.eval_count}")

    return llm_response


# async def call_llm(
#         messages: list[str],
#         model: str,
#         think: bool = False,
#         tools: list[dict[str, str]] | None = None
# ):
#     logger.info("Calling llm...")
#     ollama_client = ChatOllama(model=model)

#     llm_response = await ollama_client.ainvoke(
#         # model=model,
#         input=messages,
#         # tools=tools,
#         # think=think
#     )

#     logger.info(f"Raw LLM response: {llm_response}")

#     return llm_response