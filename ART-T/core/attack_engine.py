from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AttackState(TypedDict):
    goal: str
    attempts: int
    history: List[str]
    status: str

class AdaptiveAttacker:
    def __init__(self):
        self.workflow = self._build_graph()

    def _build_graph(self):
        # Define the nodes
        def generate_payload(state: AttackState):
            # Placeholder: In reality, call an LLM to generate attack
            print(f"[Attack] Generating payload for: {state['goal']}")
            return {"history": state["history"] + ["payload_v1"]}

        def evaluate_response(state: AttackState):
            # Placeholder: Check if attack worked
            print("[Attack] Evaluating response...")
            # Mock success for demo
            if state["attempts"] > 1:
                return {"status": "success"}
            return {"status": "failed", "attempts": state["attempts"] + 1}

        # Build Graph
        workflow = StateGraph(AttackState)
        workflow.add_node("generator", generate_payload)
        workflow.add_node("evaluator", evaluate_response)
        
        workflow.set_entry_point("generator")
        workflow.add_edge("generator", "evaluator")
        
        # Conditional Logic
        def check_success(state):
            if state["status"] == "success":
                return END
            return "generator"

        workflow.add_conditional_edges("evaluator", check_success)
        return workflow.compile()

    async def run_campaign(self, goal: str):
        initial_state = {"goal": goal, "attempts": 0, "history": [], "status": "pending"}
        result = await self.workflow.ainvoke(initial_state)
        return result