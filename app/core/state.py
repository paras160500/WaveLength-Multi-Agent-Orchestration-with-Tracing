# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps

# =========================================================================================
#                                        Class Statements
# =========================================================================================

class State(TypedDict):
    """
        State schema for multi-agent customer support workflow
    """

    # Id of the customer
    customer_id : str 

    # Conversation history 
    messages : Annotated[list[AnyMessage] , add_messages]

    # user preference and context from long-term memory
    loaded_memory : str 
    
    # Counter to prevent infinite loop
    remaining_steps : RemainingSteps