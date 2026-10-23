from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4
from .constants import DEFAULT_PORT
from pydantic import BaseModel, Field


class DeviceDiscoveryMessage(BaseModel):
    type: Literal["discovery"] = "discovery"
    device_id: str = Field(min_length=1, max_length=150)
    device_name: str = Field(min_length=1, max_length=150)
    tcp_port: int = DEFAULT_PORT
    protocol_version: int = 1 


class BaseMessage(BaseModel):
    message_id: str = Field(min_length=1, max_length=150)
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
    device_id: str = Field(min_length=1, max_length=150)
    content: str = Field(max_length=500_000)


