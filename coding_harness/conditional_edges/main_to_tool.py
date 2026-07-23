from coding_harness.states import MainAgentState

def tool_call_decision_edge(state: MainAgentState) -> bool:
    lalala= state.get("tool_calls", [])
    print(f"\n\n\n\n{lalala}\n\n\n")
    if state.get("tool_calls", []):
        return True
    return False