"""
    HTTP Endpoints exposed to React frontend 
"""

# =========================================================================================
#                                        Import Statements
# =========================================================================================

from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest,ChatResponse, NewThreadResponse, HealthResponse
from app.services import chat_service

router = APIRouter()

# =========================================================================================
#                                        routing Statements
# =========================================================================================

@router.get("/health" , response_model=HealthResponse)
async def health():
    return HealthResponse()

@router.post("/chat/thread" , response_model=NewThreadResponse)
async def new_thread():
    """
        Start a brand new conversation thread.
    """
    return NewThreadResponse(thread_id=chat_service.create_thread())

@router.post("/chat/message" , response_model=ChatResponse)
async def post_message(payload : ChatRequest):
    """
        Send a message to the multi-agent system
        If the graph is currently pause on the human in the loop interrupt for this
        thread the message is used to resume the graph instead of starting a new turn
    """
    try:
        return await chat_service.send_message(
            message=payload.message,thread_id=payload.thread_id , user_id=payload.user_id
        )
    except Exception as exc:
        raise HTTPException(status_code=500 , detail = str(exc)) from exc 

@router.get("/chat/{thread_id}/history" , response_model=ChatResponse)
async def get_history(thread_id : str):
    try:
        return await chat_service.get_history(thread_id)
    except Exception as exc:
        raise HTTPException(status_code=404 , detail=f"Thread not found : {exc}") from exc 

@router.get("/debug/memory/{customer_id}")
async def debug_memory(customer_id : str):
    """
        Inspect a customer;s saved long-term memory directly. Hany for testing that 
        preferences persist across conversations- not meant for production use.
    """
    memory = chat_service.get_Saved_memory(customer_id)
    if memory is None:
        return {'customer_id' : customer_id , "memory" : None , "note" : "No memory saved yet for this customer."}
    return {"customer_id" : customer_id , "memory" : memory}