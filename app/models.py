from sqlalchemy import Boolean, Column, String, Float, DateTime

from app import database


class sensor_data(database.Base):
    __tablename__ = "sensor_data"

    place = Column(String, primary_key=True, index=True)
    sensor_ID = Column(String, primary_key=True, index=True)
    date = Column(DateTime, primary_key=True, index=True)
    pressure = Column(Float, index=True)
    voltage = Column(Float, index=True)
    notes = Column(String, index=True)
    seqNum = Column(Float, index=True)
    aX = Column(Float, index=True)
    aY = Column(Float, index=True)
    aZ = Column(Float, index=True)
    processed = Column(Boolean, index=True)
    wtemp = Column(Float, index=True)


