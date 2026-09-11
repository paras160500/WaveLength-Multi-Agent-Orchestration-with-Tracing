"""
    Assembles the full graph:
    START -> verify_info -> (human_input loop) -> load_memory -> supervisor -> create_memory -> END
"""

# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from langgraph.graph import StateGraph, START,END

from app.core.state import State 
from app.core.llm import checkpointer, in_memory_store
from app.agents.supervisor import supervisor_prebuilt
from app.graph.verification import verify_info, human_input , should_interrupt
from app.graph.memory import load_memory, create_memory

# =========================================================================================
#                                        Agent Statements
# =========================================================================================

def build_multi_agent_graph():
    graph = StateGraph(State)

    graph.add_node("verify_info" , verify_info)
    graph.add_node("human_input" , human_input)
    graph.add_node("load_memory" , load_memory)
    graph.add_node("supervisor" , supervisor_prebuilt)
    graph.add_node("create_memory" , create_memory)

    graph.add_edge(START , "verify_info")
    graph.add_conditional_edges("verify_info" , should_interrupt , {
        "continue" : "load_memory" , "interrupt" : "human_input"
    })
    graph.add_edge("human_input" , "verify_info")
    graph.add_edge("load_memory" , "supervisor")
    graph.add_edge("supervisor" , "create_memory")
    graph.add_edge("create_memory" , END)

    return graph.compile(
        name = "multi_agent_verify",
        checkpointer=checkpointer,
        store=in_memory_store
    )

multi_agent_graph = build_multi_agent_graph()
