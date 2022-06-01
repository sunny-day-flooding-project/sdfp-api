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


class data_for_display(database.Base):
    __tablename__ = "data_for_display"

    place = Column(String, primary_key=True, index=True)
    sensor_ID = Column(String, primary_key=True, index=True)
    date = Column(DateTime, primary_key=True, index=True)
    voltage = Column(Float, index=True)
    sensor_water_depth = Column(Float, index=True)
    qa_qc_flag = Column(Boolean, index=True)
    date_surveyed = Column(DateTime, index=True)
    sensor_elevation = Column(Float, index=True)
    road_elevation = Column(Float, index=True)
    lat = Column(Float, index=True)
    lng = Column(Float, index=True)
    alert_threshold = Column(Float, index=True)
    min_water_depth = Column(Float, index=True)
    deriv = Column(Float, index=True)
    change_pt = Column(Boolean, index=True)
    smoothed_min_water_depth = Column(Float, index=True)
    sensor_water_level = Column(Float, index=True)
    road_water_level = Column(Float, index=True)
    sensor_water_level_adj = Column(Float, index=True)
    road_water_level_adj = Column(Float, index=True)


class sensor_surveys(database.Base):
    __tablename__ = "sensor_surveys"

    place = Column(String, primary_key=True, index=True)
    sensor_ID = Column(String, primary_key=True, index=True)
    date_surveyed = Column(DateTime, primary_key=True, index=True)
    sensor_elevation = Column(Float, index=True)
    road_elevation = Column(Float, index=True)
    lat = Column(Float, index=True)
    lng = Column(Float, index=True)
    alert_threshold = Column(Float, index=True)
    atm_data_src = Column(String, index=True)
    atm_station_id = Column(String, index=True)
    wl_src = Column(String, index=True)
    wl_id = Column(String, index=True)
    wl_url = Column(String, index=True)
    notes = Column(String, index=True)
    wl_types = Column(String, index=True)
    under_construction = Column(Boolean, index=True)
