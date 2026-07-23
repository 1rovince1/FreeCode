from coding_harness.states import MainAgentState

def tool_call_decision_edge(state: MainAgentState) -> bool:
    if state.get("tool_calls", []):
        return True
    return False