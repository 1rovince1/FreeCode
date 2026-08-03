import logging
from uuid import UUID
import json

from clients.redis_client import redis_manager
from coding_harness.orchestration_main_agent import compiled_harness
from config.env_config import env_settings

logger = logging.getLogger(__name__)


async def process_user_request(
        user_query: str,
        session_id: UUID
):
    logger.info(f"Processing user request (session-{session_id}): {user_query}")

    session_key = f"session-{session_id}"
    redis_session = await redis_manager.client.get(name=session_key)
    session_state = json.loads(redis_session) if redis_session else {"session_messages": []}

    session_state["session_messages"].append({
        "role": "user",
        "content": user_query
    })

    resultant_state = await compiled_harness.ainvoke(session_state)
    logger.info(f"User request processing result: {resultant_state}")

    await redis_manager.client.set(
        name=session_key,
        value=json.dumps(resultant_state),
        ex=env_settings.CHAT_SESSION_EXPIRATION_TIME
    )

    return resultant_state["session_messages"][-1]["content"]