from backend.database import SessionLocal
from backend.models import Event

def get_zone_analytics():

    db = SessionLocal()

    events = db.query(Event).all()

    zone_visits = {}

    for e in events:

        if e.event_type == "ZONE_VISIT":

            zone_visits[e.zone] = (
                zone_visits.get(e.zone, 0)
                + 1
            )

    popular_zone = None

    if zone_visits:

        popular_zone = max(
            zone_visits,
            key=zone_visits.get
        )

    db.close()

    return {
        "most_popular_zone": popular_zone,
        "zone_visits": zone_visits
    }