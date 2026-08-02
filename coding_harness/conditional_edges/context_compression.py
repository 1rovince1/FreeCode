import logging

from coding_harness.states import MainAgentState, SubAgentState
from config.env_config import env_settings

logger = logging.getLogger(__name__)


async def context_compression_decision_edge(state: MainAgentState | SubAgentState):
    logger.info("Inside context compression decision edge")

    current_session_tokens = state.get("session_current_token_count", 0)
    return_node = "continue"
    if current_session_tokens >= env_settings.CONTEXT_TOKENS_ALLOWED:
        return_node = "compress"

    logger.info("Exiting context compression decision edge")
    return return_node