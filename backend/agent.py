



from transformers import pipeline
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    output: str


qa_pipeline = pipeline("text-generation", model="gpt2")


@tool
def booking(details: str) -> str:
    """ BOOKING"""
    try:
        date, time, summary = map(str.strip, details.split(',', 2))
        return f"📅 Event booked on {date} at {time}: {summary}"
    except ValueError:
        return (
            "❌ Error: Provide 3 values - date, time, summary "
            "(e.g., '2025-07-10, 14:00, Team Sync')"
        )


def hf_wrapper(prompt: str) -> str:
    result = qa_pipeline(prompt, max_new_tokens=100)[0]["generated_text"]
    return result.strip()


llm_runnable = RunnableLambda(hf_wrapper)


def process_input(state):
    user_input = state["input"]
    result = hf_wrapper(user_input)
    return {"output": result}

def route_tool(state):
    text = state["output"]
    
    if "book" in text.lower():
        return "booking"
    return END

def run_booking(state):
    
    try:
        msg = state["input"]
        details = msg.split("using", 1)[-1].strip()
        return {"output": booking(details)}
    except:
        return {"output": "❌ Could not extract event details."}


graph = StateGraph(state_schema=AgentState)

graph.add_node("llm", process_input)
graph.add_node("booking", run_booking)

graph.set_entry_point("llm")
graph.add_conditional_edges("llm", route_tool, {
    "booking": "booking",
    END: END
})
graph.add_edge("booking", END)

# Export the executable graph
calendar_agent = graph.compile()
