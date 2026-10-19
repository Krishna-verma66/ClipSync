from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    message_id: UUID = Field(default_factory=uuid4)
    protocol_version: int = 1
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ConnectMessage(BaseMessage):
    type: Literal["connect"] = "connect"
    device_id: UUID
    device_name: str = Field(min_length=1, max_length=100)



class ClipboardUpdateMessage(BaseMessage):
    type: Literal["clipboard_update"] = "clipboard_update"
    device_id: UUID
    content: str = Field(max_length=500_000)


class AckMessage(BaseMessage):
    type: Literal["ack"] = "ack"
    acknowledged_message_id: UUID
    success: bool = True


class ErrorMessage(BaseMessage):
    type: Literal["error"] = "error"
    code: str
    detail: str
