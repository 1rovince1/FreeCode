from pydantic import BaseModel, Field


class ExcuteShellCommand(BaseModel):
    command: str = Field(..., description="Command to execute.")
