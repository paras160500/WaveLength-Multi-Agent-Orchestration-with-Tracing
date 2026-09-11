"""
Pydantic models for the chat API's request/response bodies
"""
# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from typing import List,Literal, Optional
from pydantic import BaseModel, Field

# =========================================================================================
#                                        Class Statements
# =========================================================================================

class ChatMessage(BaseModel):
    role : Literal["user" , "assistant" , "system"]
    name : Optional[str] = None 
    content : str 

class TraceEvent(BaseModel):
    """
        One step of agent activity for the live trace panel.
    """
    agent : str = Field(... , description="Which agent produced this step (supervisor, invoice_information_subagent, ...).")
    action : Literal['routing' , 'tool_call' , 'tool_result' , 'responded' , 'verifying' , 'verified']
    label : str = Field(... , description="Short human-readable summary of what happened.")
    detail : Optional[str] = Field(None , description="Extra detail (tool args , truncated content).")

class MemoryProfile(BaseModel):
    customer_id : str 
    music_preferences : List[str] = []

class ChatRequest(BaseModel):
    """
        Sent by the frontend for every thun of the conversation
    """
    message : str = Field(... , description="The user's message text.")
    thread_id : Optional[str] = Field(None , description="Existing conversation thread ID. Omit to start a new conversation")
    user_id : Optional[str] = Field(None , description="Stable ID used for long-term memory lookup (defaults to customer_id once verified).")

class ChatResponse(BaseModel):
    thread_id : str 
    messages : List[ChatMessage]
    awaiting_input : bool = Field(False , description="True if the graph is paused on a human-in-the-loop interrupt.")
    customer_id : Optional[str] = None 
    trace : List[TraceEvent] = Field(None , description="The customer;s current saved long-term memory, if verified.")
    memory : Optional[MemoryProfile] = Field(None , description="The customer's current saved long-term memory, if verified.")

class NewThreadResponse(BaseModel):
    thread_id : str 

class HealthResponse(BaseModel):
    status : str = "ok"