import logging

from fastapi import APIRouter, status, HTTPException

from services.chat_session import get_all_active_sessions


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/create_session")
async def create_session_request():
    import uuid
    return {
        "message": "Session created",
        "session_id": uuid.uuid4()
    }


@router.get("/all_active_sessions")
async def get_all_active_sessions_request():
    try:
        active_sessions = await get_all_active_sessions()
        return {
            "active_sessions": active_sessions
        }
    except Exception as e:
        logger.exception("Error while processing request", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while processing request"
        )