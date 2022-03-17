from pydantic import BaseModel
# Need to import List function for wl_types
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


class add_survey(BaseModel):
    place: str
    sensor_ID: str
    date_surveyed: str
    sensor_elevation: float
    road_elevation: float
    lat: float
    lng: float
    alert_threshold: float
    atm_data_src: str
    atm_station_id: str
    wl_src: str
    wl_id: str
    wl_url: str
    notes: str = ""
    wl_types: str

    class Config:
        orm_mode = True