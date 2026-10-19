from database import engine, repository, models
import uuid


session = engine.SessionLocal()

"""device = repository.register_device(
    db=session,
    device_uid=str(uuid.uuid1()),
    name="Desktop Wn1"
)

session.commit()"""


devices = repository.get_all_devices(db=session)

print(devices)