# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from typing import List 
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore 

from app.core.state import State 
from app.core.llm import llm 

# =========================================================================================
#                                        Agent Statements
# =========================================================================================

class UserProfile(BaseModel):
    customer_id : str = Field(description="The custoemr ID of the customer")
    music_preferences: list[str] = Field(
        default_factory=list,
        description="The music preferences of the customer"
    )


CREATE_MEMORY_PROMPT = """
    You are an expert analyst that is observing a conversation that has taken place between a customer and a customer support assistant. The customer support assistant works for a digital music store, and has utilized a multi-agent team to answer the customer's request.
    You are tasked with analyzing the conversation that has taken place between the customer and the customer support assistant, and updating the memory profile associated with the customer. The memory profile may be empty. If it's empty, you should create a new memory profile for the customer.

    You specifically care about saving any music interest the customer has shared about themselves, particularly their music preferences to their memory profile.

    To help you with this task, I have attached the conversation that has taken place between the customer and the customer support assistant below, as well as the existing memory profile associated with the customer that you should either update or create.

    The customer's memory profile should have the following fields:
    - customer_id: the customer ID of the customer
    - music_preferences: the music preferences of the customer

    These are the fields you should keep track of and update in the memory profile. If there has been no new information shared by the customer, you should not update the memory profile. It is completely okay if you do not have new information to update the memory profile with. In that case, just leave the values as they are.

    *IMPORTANT INFORMATION BELOW*

    The conversation between the customer and the customer support assistant that you should analyze is as follows:
    {conversation}

    The existing memory profile associated with the customer that you should either update or create based on the conversation is as follows:
    {memory_profile}

    Ensure your response is an object that has the following fields:
    - customer_id: the customer ID of the customer
    - music_preferences: the music preferences of the customer

    For each key in the object, if there is no new information, do not update the value, just keep the value that is already there. If there is new information, update the value.

    Take a deep breath and think carefully before responding.
"""

def format_user_memory(user_data) -> str:
    profile = user_data['memory']
    if hasattr(profile , "music_preferences") and profile.music_preferences:
        return f"Music Preferences : {', '.join(profile.music_preferences)}"
    return ""

def load_memory(state : State , config : RunnableConfig , store : BaseStore):
    user_id = str(config['configurable'].get("user_id" , state['customer_id']))
    namespace = ("memory_profile" , user_id)

    existing_memory = store.get(namespace , "user_memory")
    formatted_memory = ""
    if existing_memory and existing_memory.value:
        formatted_memory = format_user_memory(existing_memory.value)

    return {"loaded_memory" : formatted_memory}


def create_memory(state : State , config : RunnableConfig , store : BaseStore):
    user_id = str(config['configurable'].get("user_id" , state['customer_id']))
    namespace = ("memory_profile" , user_id)

    existing_memory = store.get(namespace , "user_memory")
    formatted_memory = ""

    if existing_memory and existing_memory.value:
        profile = existing_memory.value.get("memory")

        if profile and profile.music_preferences:
            formatted_memory = f"Music Preferences : {', '.join(profile.music_preferences)}"


    system_message = SystemMessage(content=CREATE_MEMORY_PROMPT.format(
        conversation=state['messages'], memory_profile = formatted_memory
    ))

    updated_memory = llm.with_structured_output(UserProfile).invoke([system_message])
    store.put(namespace , "user_memory" , {"memory" : updated_memory})