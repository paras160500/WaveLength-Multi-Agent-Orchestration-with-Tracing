# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from langgraph_supervisor import create_supervisor

from app.core.state import State
from app.core.llm import llm,checkpointer,in_memory_store
from app.agents.music_agent import music_catalog_subagent
from app.agents.invoice_agent import invoice_information_subagent

# =========================================================================================
#                                        Agent Statements
# =========================================================================================

SUPERVISOR_PROMPT = """
    You are an expert customer support assistant for a digital music store.
    You are dedicated to providing exceptional service and ensuring customer queries are answered thoroughly.
    You have a team of subagents that you can use to help answer queries from customers.
    Your primary role is to serve as a supervisor/planner for this multi-agent team that helps answer queries from customers.

    Your team is composed of two subagents that you can use to help answer the customer's request:
    1. music_catalog_subagent: this subagent has access to user's saved music preferences. It can also retrieve information about the digital music store's music
    catalog (albums, tracks, songs, etc.) from the database.
    2. invoice_information_subagent: this subagent is able to retrieve information about a customer's past purchases or invoices
    from the database.

    Based on the existing steps that have been taken in the messages, your role is to generate the next subagent that needs to be called.
    This could be one step in an inquiry that needs multiple sub-agent calls.
"""

def build_supervisor():
    supervisor_workflow = create_supervisor(
        agents=[invoice_information_subagent , music_catalog_subagent],
        output_mode="last_message",
        model=llm,
        prompt = SUPERVISOR_PROMPT,
        state_schema = State 
    )
    return supervisor_workflow.compile(
        name = "supervisor", checkpointer=checkpointer , store = in_memory_store
    )

supervisor_prebuilt = build_supervisor()