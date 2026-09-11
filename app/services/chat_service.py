"""
    Thin service layer between the FastAPI routes and the compiled langgraph
    multi-agent graph.Handles thread bookkeeping, the human-in-the-loop interrupt/resume
    flow, live agent-activity trace events, and long-term memory lookups for 
    the frontend's memory panel.
"""

# =========================================================================================
#                                        Import Statements
# =========================================================================================

import uuid 
from typing import Dict, List, Optional

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.graph.workflow import multi_agent_graph
from app.models.schemas import ChatMessage, ChatResponse , MemoryProfile , TraceEvent

# Tracks wchich thread_ids are currently paused on a human-in-the-loop interrupt.
_pending_interrupts : Dict[str,bool] = {}

# Track how many messages of each thread's fully history have already been returned to the 
# client, so send_message only ever ships the new onces
_last_sent_count : Dict[str , int] = {}

# Handoff tool names created by langgraph-supervisor for each sub-agent.
_HANDOFF_TOOL_NAMES = {
    "transfer_to_invoice_information_subagent",
    "transfer_to_music_catalog_subagent",
    "transfer_back_to_supervisor",
}

_AGENT_DISPLAY_NAMES = {
    "supervisor": "Supervisor",
    "invoice_information_subagent": "Billing agent",
    "music_catalog_subagent": "Catalog agent",
    "verification": "Verification",
}


# =========================================================================================
#                                        logic Statements
# =========================================================================================

def _display_name(agent_key : str) -> str:
    return _AGENT_DISPLAY_NAMES.get(agent_key , agent_key)

def create_thread() -> str:
    return str(uuid.uuid4())

def _is_handoff_artifact(msg) -> bool:
    """
        True for supervisor handoff plumbing that shoulnot reach the user
        as chat text
    """
    tool_calls = getattr(msg , "tool_calls" , None) or []
    if any(tc.get("name") in _HANDOFF_TOOL_NAMES for tc in tool_calls):
        return True 
    msg_type = getattr(msg , "type" , None)
    content = msg.content if isinstance(msg.content , str) else ""
    if msg_type == "tool" and (
        "Successfully transferred" in content or "transferred back to supervisor" in content ):
        return True 
    return False 

def _extract_messages(raw_messages) -> List[ChatMessage]:
    """
        Clean user-facing chat transcript 
    """
    chat_messages : List[ChatMessage] = []
    for msg in raw_messages:
        if _is_handoff_artifact(msg):
            continue

        msg_type = getattr(msg , "type" , None)
        role = "assistant"
        if msg_type == "human":
            role = "user"
        elif msg_type == "system":
            role = "system"

        content = msg.content if isinstance(msg.content , str) else str(msg.content)
        if not content:
            continue

        chat_messages.append(
            ChatMessage(role = role , name=getattr(msg , "name" , None) , content = content)
        )

    return chat_messages


def _build_trace(raw_messages) -> List[TraceEvent]:
    """
        Turn the raw new messages from this turn into a feed of agent-activity
        events for the frontend's live-trace panel: Who did what in order
    """
    events = List[TraceEvent] = []

    for msg in raw_messages:
        msg_type = getattr(msg , "type" , None)
        name = getattr(msg , "name" , None)
        tool_calls = getattr(msg, "tool_calls", None) or []

        content = msg.content if isinstance(msg.content , str) else ""

        if msg_type == "system" and "verify" in content.lower():
            events.append(
                TraceEvent(agent = _display_name("verification") , action="verified" , label=content)
            )
            continue

        for tc in tool_calls:
            tool_name = tc.get("name" , "")
            if tool_name == "transfer_back_to_supervisor":
                events.append(
                    TraceEvent(
                        agent=_display_name(name or "agent"),
                        action="routing",
                        label="Handing control back to the supervisor"
                    )
                )
            elif tool_name in _HANDOFF_TOOL_NAMES:
                target = tool_name.replace("transfer_to_" , "")
                events.append(
                    TraceEvent(agent=_display_name("supervisor"),action="routing" ,
                                label=f"Routing to {_display_name(target)}")
                )
            elif tool_name:
                events.append(
                    TraceEvent(
                        agent=_display_name(name or "agent"),
                        action = "tool_call",
                        label=f"Calling {tool_name}",
                        detail=str(tc.get("args")) if tc.get("args") else None
                    )
                )

        if msg_type == "tool" and not _is_handoff_artifact(msg) and content:
            events.append(
                TraceEvent(
                    agent=_display_name(name or "tool"),
                    action = "tool_result",
                    label = "tool returned a result",
                    detail=content[:200]
                )
            )

        if msg_type == "ai" and not tool_calls and content:
            events.append(
                TraceEvent(
                    agent=_display_name(name or "supervisor"),
                    action="responded",
                    label=content[:160]
                )
            )

    return events 

def get_Saved_memory(customer_id : str) -> Optional[MemoryProfile]:
    """
        Directly read a customer's stored long-term memory
    """
    from app.core.llm import in_memory_store

    namesapce = ("memory_profile" , str(customer_id))
    record = in_memory_store.get(namesapce , "user_memory")
    if not record or not record.value:
        return None 

    profile = record.value.get("memory")
    if profile is None:
        return None 

    return MemoryProfile(customer_id=str(profile.customer_id) , music_preferences=profile.music_preferences)


async def send_message(message : str , thread_id : str | None , user_id : str | None) -> ChatResponse:
    if thread_id is None:
        thread_id = create_thread()

    # Only pass an explicit user_id if the frontend actually has not yet
    # After this customer has been verified in an earlier turn
    # Otherwise leave it out so load_memory/create_memory fall back to the 
    # customer_id that verify_info just set in the graph;s own state- the stable,
    # cross-session key memory should actually be saved under.

    configurable = {"thread_id" : thread_id}
    if user_id:
        configurable['user_id'] = user_id
    config = {"configurable" : configurable}

    if _pending_interrupts.get(thread_id):
        result = await multi_agent_graph.ainvoke(Command(resume = message) , config=config)
    else:
        result = await multi_agent_graph.ainvoke(
            {"messages" : [HumanMessage(content = message)]} , config=config
        )

    if "__interrupt__" in result:
        _pending_interrupts[thread_id] = True 
        prompt_text = result['__interrupt__'][0].value
        return ChatResponse(
            thread_id=thread_id , 
            messages=[ChatMessage(role = "assistant" , content = prompt_text)],
            awaiting_input=True,
            customer_id = None,
            trace = [
                TraceEvent(
                    agent=_display_name("verification"),
                    action="verifying",
                    label="Waiting for customer ID,email or phone number"
                )
            ],
            memory = None 
        )

    _pending_interrupts.pop(thread_id , None)

    # Only process messages the client hasn't seen yet for this thread.
    all_messages = result['messages']
    already_sent = _last_sent_count.get(thread_id , 0)
    new_messages = all_messages[already_sent : ]
    _last_sent_count[thread_id] = len(all_messages)

    customer_id = result.get("customer_id")
    memory = get_Saved_memory(customer_id) if customer_id else None 

    return ChatResponse(
        thread_id=thread_id,
        messages=_extract_messages(new_messages),
        awaiting_input=False,
        customer_id=str(customer_id) if customer_id else None,
        trace=_build_trace(new_messages),
        memory = memory
    )


async def get_history(thread_id : str) -> ChatResponse:
    config = {"configurable" : {"thread_id" : thread_id}}
    state = await multi_agent_graph.aget_state(config)
    values = state.values or {} 
    customer_id = values.get("customer_id")
    return ChatResponse(
        thread_id=thread_id,
        messages = _extract_messages(values.get("messages" , [])),
        awaiting_input=_pending_interrupts.get(thread_id , False),
        customer_id = str(customer_id) if customer_id else None ,
        trace = [],
        memory = get_Saved_memory(customer_id) if customer_id else None 
    )