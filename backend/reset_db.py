from backend.database import SessionLocal
from backend.models import Event

db = SessionLocal()

db.query(Event).delete()

db.commit()

db.close()

print("Database Cleared")