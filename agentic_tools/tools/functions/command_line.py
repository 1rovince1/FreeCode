import subprocess

ALLOWED_CMDS = ["ls", "pwd", "whoami", "df", "free"]

async def execute_shell_command(command: str):
    f"""
    Execute a shell command and return its output
    Allowed cmds: {ALLOWED_CMDS}
    """
    try:
        print(f"command request: {command}")
        if command.split()[0] not in ALLOWED_CMDS:
            return "Error: Command not allowed"
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return result.stdout.strip() if result.stdout else "Command executed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"
