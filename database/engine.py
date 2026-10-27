from sqlalchemy import create_engine
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

DATABASE_URL = "sqlite:///clipsync.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
) 

with engine.connect() as conn:
    result = conn.exec_driver_sql("insert into devices (device_uid, name, created_at) values (?, ?, ?), (?, ?, ?);", (str(uuid4()), "Krishna's Desktop", datetime.now(timezone.utc), str(uuid4()), "Chaman's Desktop", datetime.now(timezone.utc)))

    result = conn.exec_driver_sql("select * from devices;")
    for data in result:
        print(data)



SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)