from backend.database import SessionLocal
from backend.models import Event

db = SessionLocal()

events = db.query(Event).all()

print(f"Total Events: {len(events)}")

for e in events:

    print(
        e.id,
        e.person_id,
        e.event_type,
        e.camera_id,
        e.zone,
        e.timestamp
    )

db.close()