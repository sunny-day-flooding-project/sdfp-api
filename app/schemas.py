from pydantic import BaseModel, Field
from typing import Dict
# Need to import List function for wl_types
import datetime


class sensor_data_ingest(BaseModel):
    place: str = Field(..., example="Beaufort, North Carolina")
    sensor_ID: str = Field(..., example="BF_01")
    date: str = Field(..., example="2022-03-16 10:13:09.148658-04:00")
    pressure: float = Field(..., example = "1000")
    raw_pressure: float | None
    wtemp: float = Field(..., example = "25")
    notes: str = Field("", example = "test")
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
    place: str = Field(..., example="Beaufort, North Carolina")
    sensor_ID: str = Field(..., example="BF_01")
    date_surveyed: str = Field(..., example="20220201000000")
    sensor_elevation: float = Field(..., example=-1)
    road_elevation: float = Field(..., example=2)
    lat: float = Field(..., example=34)
    lng: float = Field(..., example=-76)
    alert_threshold: float = Field(..., example=1.5)
    atm_data_src: str = Field(..., example="NOAA")
    atm_station_id: str = Field(..., example="8656483")
    wl_src: str = Field(..., example="NOAA")
    wl_id: str = Field(..., example=8656483)
    wl_url: str = Field(..., example="https://tidesandcurrents.noaa.gov/waterlevels.html?id=8656483")
    notes: str = Field("", example="test")
    wl_types: str = Field(..., example="obs")
    under_construction: bool = Field(..., example=False)
    sensor_label: str = Field(..., example="Starfish Ln. at Canal Dr.")
    alt_wl_src: str = Field("", example="NOAA") 
    alt_wl_id: str = Field("", example="8656483") 
    alt_wl_url: str = Field("", example="https://tidesandcurrents.noaa.gov/waterlevels.html?id=8656483") 
    alt_wl_types: str = Field("", example="obs") 
    alt_atm_data_src: str = Field("", example="NOAA")
    alt_atm_station_id: str = Field("", example="8656483")
    reference_elevation: float = Field(..., example=1.0)
    reference_elevation_type: str = Field("", example="drain_bottom") 

    class Config:
        orm_mode = True

class ml_camera_data_ingest(BaseModel):
    device: str = Field(..., example="dev:94deb8230136")
    when: str = Field(..., example="1711400133")
    body: Dict = Field(..., example="JSON structure containing floodstatus field")

    class Config:
        orm_mode = True
        extra = 'ignore'