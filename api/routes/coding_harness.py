
import logging

from fastapi import APIRouter, status, HTTPException
# from harnesses.coding_harness.orchestration import compiled_harness
from services.chat_session import process_user_request
from api.models.chat import ChatRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/request_agent")
async def request_to_agent(request: ChatRequest):
    # await compiled_harness.ainvoke({
    #     "main_agent_messages": []
    # })
    try:
        result = await process_user_request(
            user_query=request.user_query,
            session_id=request.session_id
        )
        return {
            "session_id": request.session_id,
            "ai_respsonse": result
        }
    except Exception as e:
        logger.error("Error while processing request", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user request"
        )

@router.get("/create_session")
async def create_session_request():
    import uuid
    return {
        "message": "Session created",
        "session_id": uuid.uuid4()
    }