from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from backend.database import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    person_id = Column(Integer)

    event_type = Column(String)

    camera_id = Column(String)

    zone = Column(String, nullable=True)

    timestamp = Column(DateTime)