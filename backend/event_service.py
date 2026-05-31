from datetime import datetime

from backend.database import SessionLocal
from backend.models import Event


def save_event(
    person_id,
    event_type,
    camera_id,
    zone=None
):

    db = SessionLocal()

    event = Event(
        person_id=person_id,
        event_type=event_type,
        camera_id=camera_id,
        zone=zone,
        timestamp=datetime.now()
    )

    db.add(event)

    db.commit()

    db.close()