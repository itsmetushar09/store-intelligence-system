from backend.database import SessionLocal
from backend.models import Event


def get_heatmap_data():

    db = SessionLocal()

    events = db.query(Event).all()

    heatmap = {}

    for e in events:

        if e.zone:

            heatmap[e.zone] = (
                heatmap.get(e.zone, 0)
                + 1
            )

    db.close()

    return heatmap