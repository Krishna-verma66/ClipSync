
import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from database.models import Device, Connection, MessageRecord


# 1. Register a new device
def register_device(
    db: Session,
    device_uid: str,
    name: str,
) -> Device:
    device = Device(
        device_uid=device_uid,
        name=name,
    )

    db.add(device)
    db.flush()

    return device




# 2. Get List of Devices Connected Ever.
def get_all_devices(db: Session) -> list[Device]:
    statement = select(Device)
    return list(db.scalars(statement).all())


# 2. Find a device using its unique identifier
def get_device_by_uid(
    db: Session,
    device_uid: str,
) -> Device | None:
    statement = select(Device).where(
        Device.device_uid == device_uid
    )

    return db.scalar(statement)


# 3. Record a new connection
def create_connection(
    db: Session,
    device_id: int,
) -> Connection:
    connection = Connection(
        device_id=device_id,
        connected_at=datetime.now(timezone.utc),
        status="connected",
    )

    db.add(connection)
    db.flush()

    return connection


# 4. Mark a connection as disconnected
def close_connection(
    db: Session,
    connection_id: int,
) -> Connection | None:
    connection = db.get(Connection, connection_id)

    if connection is None:
        return None

    connection.disconnected_at = datetime.now(timezone.utc)
    connection.status = "disconnected"

    db.flush()

    return connection


# 5. Save a message
def save_message(
    db: Session,
    connection_id: int,
    message_type: str,
    payload: dict,
    message_uid: str | None = None,
) -> MessageRecord:
    message = MessageRecord(
        message_uid=message_uid or str(uuid4()),
        connection_id=connection_id,
        message_type=message_type,
        payload=json.dumps(payload),
        created_at=datetime.now(timezone.utc),
    )

    db.add(message)
    db.flush()

    return message


# 6. Retrieve the latest messages
def get_recent_messages(
    db: Session,
    connection_id: int,
    limit: int = 20,
) -> list[MessageRecord]:
    limit = max(1, min(limit, 100))

    statement = (
        select(MessageRecord)
        .where(MessageRecord.connection_id == connection_id)
        .order_by(desc(MessageRecord.created_at))
        .limit(limit)
    )

    return list(db.scalars(statement).all())
