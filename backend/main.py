from fastapi import FastAPI

from backend.database import SessionLocal
from backend.models import Event
from backend.analytics import get_zone_analytics
from backend.heatmap import get_heatmap_data

app = FastAPI(
    title="Store Intelligence API"
)

# -------------------------
# EVENTS
# -------------------------

@app.get("/events")
def get_events():

    db = SessionLocal()

    events = db.query(Event).all()

    result = []

    for e in events:

        result.append({
            "id": e.id,
            "person_id": e.person_id,
            "event_type": e.event_type,
            "camera_id": e.camera_id,
            "zone": e.zone,
            "timestamp": str(e.timestamp)
        })

    db.close()

    return result


# -------------------------
# METRICS
# -------------------------

@app.get("/metrics")
def get_metrics():

    db = SessionLocal()

    events = db.query(Event).all()

    entries = 0
    exits = 0

    unique_people = set()

    zone_counts = {}

    for e in events:

        unique_people.add(e.person_id)

        if e.event_type == "ENTRY":
            entries += 1

        elif e.event_type == "EXIT":
            exits += 1

        elif e.event_type == "ZONE_VISIT":

            zone = e.zone

            zone_counts[zone] = (
                zone_counts.get(zone, 0) + 1
            )

    popular_zone = None

    if zone_counts:

        popular_zone = max(
            zone_counts,
            key=zone_counts.get
        )

    db.close()

    return {
        "total_entries": entries,
        "total_exits": exits,
        "unique_visitors": len(unique_people),
        "most_popular_zone": popular_zone,
        "zone_visits": zone_counts
    }


# -------------------------
# FUNNEL
# -------------------------

@app.get("/funnel")
def get_funnel():

    db = SessionLocal()

    events = db.query(Event).all()

    entered = set()
    zone_visitors = set()

    for e in events:

        if e.event_type == "ENTRY":
            entered.add(e.person_id)

        if e.event_type == "ZONE_VISIT":
            zone_visitors.add(e.person_id)

    conversion_rate = 0

    if len(entered) > 0:

        conversion_rate = (
            len(zone_visitors)
            / len(entered)
        ) * 100

    db.close()

    return {
        "entered_store": len(entered),
        "engaged_customers": len(zone_visitors),
        "engagement_rate": round(
            conversion_rate,
            2
        )
    }


# -------------------------
# ANOMALIES
# -------------------------

@app.get("/anomalies")
def get_anomalies():

    db = SessionLocal()

    events = db.query(Event).all()

    entries = sum(
        1
        for e in events
        if e.event_type == "ENTRY"
    )

    exits = sum(
        1
        for e in events
        if e.event_type == "EXIT"
    )

    db.close()

    anomalies = []

    if entries > 20:

        anomalies.append(
            "High Footfall Detected"
        )

    if exits > entries:

        anomalies.append(
            "More Exits Than Entries"
        )

    return {
        "anomalies": anomalies
    }


# -------------------------
# ANALYTICS
# -------------------------

@app.get("/analytics")
def analytics():

    return get_zone_analytics()

@app.get("/heatmap")
def heatmap():

    return get_heatmap_data()


@app.get("/")
def home():
    return {
        "project": "Store Intelligence System",
        "status": "running",
        "docs": "/docs"
    }