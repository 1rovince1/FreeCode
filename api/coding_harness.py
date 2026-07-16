
import logging

from fastapi import APIRouter, status, HTTPException
from harnesses.coding_harness.orchestration import compiled_harness

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/request_agent")
async def request_to_agent():
    await compiled_harness.ainvoke({
        "main_agent_messages": []
    })
    return {
        "status": "OK",
        "message": "FastAPI server is up and running!"
    }