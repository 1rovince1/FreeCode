import logging
from uuid import UUID
import json

from clients.redis_client import redis_manager
from coding_harness.orchestration import compiled_harness
from helpers.message_utils import normalize_messages
from config.env_config import env_settings

logger = logging.getLogger(__name__)


async def process_user_request(
        user_query: str,
        session_id: UUID
):
    logger.info(f"Processing user request (session-{session_id}): {user_query}")

    session_key = f"session-{session_id}"
    redis_session = await redis_manager.client.get(name=session_key)
    session_data = json.loads(redis_session) if redis_session else {"session_messages": []}
    session_messages = session_data["session_messages"]

    session_messages.append({
        "role": "user",
        "content": user_query
    })

    result = await compiled_harness.ainvoke({
        "session_messages": session_messages
    })
    logger.info(f"User request processing result: {result}")

    workflow_messages = result.get("session_messages", [])
    workflow_messages = normalize_messages(workflow_messages)

    await redis_manager.client.set(
        name=session_key,
        value=json.dumps({"session_messages": workflow_messages}),
        ex=env_settings.CHAT_SESSION_EXPIRATION_TIME
    )

    return workflow_messages[-1]["content"]