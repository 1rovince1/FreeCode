from agentic_tools.tools import *

TOOLS = {
    "execute_shell_command": {
        "callable_fn": execute_shell_command,
        "description": execute_shell_command.__doc__.strip(),
        "input_schema": ExcuteShellCommand
    },
    "invoke_generic_sub_agent": {
        "description": "General reasoning sub-agent with tools",
        "input_schema": SubAgentTool
    }
}