from pydantic import BaseModel
import datetime


class sensor_data_ingest(BaseModel):
    place: str
    sensor_ID: str
    date: str
    pressure: float
    wtemp: float
    notes: str = ""
    voltage: float = 4.0
    seqNum: float = 1.0
    aX: float = 1.0
    aY: float = 1.0
    aZ: float = 1.0
    processed: bool = False
    timezone: str = 'EST'

    class Config:
        orm_mode = True