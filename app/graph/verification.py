"""
    Customer Identity verification
"""

# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

import ast
from typing import Optional

from pydantic import BaseModel, Field 
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt

from app.core.state import State 
from app.core.llm import llm 
from app.database import db 

# =========================================================================================
#                                        Agent Statements
# =========================================================================================

class UserInput(BaseModel):
    """
        Schema for parsing user-provided account information
    """
    identifier : str = Field(description = "Identifier, which can be a customer ID, email or phone number.")

structured_llm = llm.with_structured_output(UserInput)

STRUCTURED_SYSTEM_PROMPT = """
    You are a customer service representative responsible for extracting customer identifier.
    Only extract the customer's account information from the message history.
    If they haven't provide the information yet, return an empty string for the identifier.
"""

def get_customer_id_from_identifier(identifier : str) -> Optional[int]:
    """
        Resolve a customer ID , phone number or email into a numeri CustomerId
    """
    #  If it Digit
    if identifier.isdigit():
        return int(identifier)

    # If its with phone
    if identifier.startswith("+"):
        query = f"SELECT CustomerId FROM Customer WHERE Phone='{identifier}'"
        result = db.run(query)
        formatted = ast.literal_eval(result)
        if formatted:
            return formatted[0][0]

    # If it have email
    elif "@" in identifier:
        query = f"SELECT CustomerId FROM Customer WHERE Email='{identifier}'"
        result = db.run(query)
        formatted = ast.literal_eval(result)
        if formatted:
            return formatted[0][0]

    return None 


def verify_info(state : State , config : RunnableConfig):
    """
        Extract + validate a customer identifier from the latest user message.
    """

    if state.get("customer_id"):
        return {}

    system_instruction = """
    You are a music store agent, where you are trying to verify the customer identity as the first
    step of the customer support process.
    Only after thei account is verified you would be able to support them on resolving the issue.
    In order to verify their identity one of their customer ID, email or phone number needs to be provided.
    If the customer has not provided the inforamation yet,please ask them for it.
    If they have provided the identifier but cannot be found, please ask them to revise it.
    """

    user_input = state['messages'][-1]
    parsed_info = structured_llm.invoke([SystemMessage(content = STRUCTURED_SYSTEM_PROMPT)] + [user_input])
    identifier = parsed_info.identifier

    customer_id = ""
    if identifier:
        customer_id = get_customer_id_from_identifier(identifier)

    if customer_id:
        intent_message = SystemMessage(content = f"Thank you for providing your information! I was able to verify your account with customer id {customer_id}")
        return {"customer_id" : customer_id , "messages" : [intent_message]}

    response = llm.invoke([SystemMessage(content = system_instruction)] + state['messages'])
    return {"messages" : [response]}

def human_input(state : State , config : RunnableConfig):
    """
        Pause the graph and wait for the user to supply verification info
    """
    user_input = interrupt("Please provide input")
    return {"messages" : [user_input]}

def should_interrupt(state : State , config : RunnableConfig):
    return "continue" if state.get("customer_id") else "interrupt"