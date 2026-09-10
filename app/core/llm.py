"""
Singletons for LLM Client and the short/long-term memory stores.
So we dont have each time different store and different LLM.
"""
# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

import os

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from app.config import settings

# =========================================================================================
#                                        Class Statements
# =========================================================================================

# ---------------------------------Wire up the ENV variables--------------------------------

# Openai
os.environ.setdefault("OPENAI_API_KEY" , settings.openai_api_key)

# Langmsith
if settings.langsmith_api_key:
    os.environ.setdefault("LANGSMITH_API_KEY" , settings.langsmith_api_key)
    os.environ['LANGSMITH_TRACING'] = "true" if settings.langsmith_tracing else "false"
    os.environ.setdefault("LANGSMITH_PROJECT" , settings.langsmith_project)

# Main llm 
llm = ChatOpenAI(model = settings.openai_model , temperature=0 , api_key=settings.openai_api_key)

# Long-term memory : persists user preferences across conversations/thread
in_memory_store = InMemoryStore()

# Short-term memory : persists a single conversation thread's state 
checkpointer = MemorySaver()