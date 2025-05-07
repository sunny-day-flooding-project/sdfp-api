from sqlalchemy import asc, desc, and_
from sqlalchemy.orm import Session

from app import models, schemas
from datetime import datetime, timezone
from enum import Enum

def get_latest_measurement(db: Session, sensor_ID: str):
    return db.query(models.sensor_data).filter(models.sensor_data.sensor_ID == sensor_ID).order_by(
        desc('date')).first()


def get_surveys(db: Session, sensor_ID: str):
    return db.query(models.sensor_surveys).filter(models.sensor_surveys.sensor_ID == sensor_ID).order_by(
        desc('date_surveyed')).all()


def get_all_surveys(db: Session):
    return db.query(models.sensor_surveys).order_by(
        desc('date_surveyed')).all()

def get_api_data(db: Session, id: str, api_name: str, type: str, min_date: datetime, max_date: datetime):
    return db.query(models.api_data).filter(and_(
        models.api_data.date >= min_date,
        models.api_data.date <= max_date,
        models.api_data.id == id,
        models.api_data.api_name == api_name,
        models.api_data.type == type,
    )).all()

def write_new_measurements(db: Session, data: schemas.sensor_data_ingest):
    values = data.dict()
    del values["timezone"]

    string_date = values["date"]
    values["date"] = datetime.fromisoformat(string_date).replace(microsecond=0)

    new_measurements = models.sensor_data(**values)

    record_in_db = db.query(models.sensor_data).filter(and_(
        models.sensor_data.date == new_measurements.date,
        models.sensor_data.sensor_ID == new_measurements.sensor_ID,
        models.sensor_data.place == new_measurements.place
    )).all()

    if len(record_in_db) > 0:
        return "Record already in database. Measurement not written"

    if len(record_in_db) == 0:
        db.add(new_measurements)
        db.commit()
        db.refresh(new_measurements)

        diff = datetime.now(timezone.utc) - new_measurements.date
        # Log entry if greater than 24 hours ago
        if (diff.total_seconds() / 60 > 1440):
            f = open("/data-api-log/delayed_measurements.txt", "a")
            header = "date_added;place;sensor_ID;date"
            f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ";" + str(new_measurements) + "\n")
            f.close()

        return "SUCCESS! Record written to database"


# Define the enum for allowed values
class DataMode(str, Enum):
    unmasked = "unmasked"
    masked = "masked"

def get_water_level(db: Session, min_date: datetime, max_date: datetime, sensor_ID: str, mode: str):
    nan_threshold = 1 / 6
    
    qresults = db.query(models.data_for_display).filter(and_(
        models.data_for_display.date >= min_date,
        models.data_for_display.date <= max_date,
        models.data_for_display.sensor_ID == sensor_ID
    )).all()

    if mode == DataMode.masked:
        for row in qresults:
            if (
                row.sensor_water_level_adj is not None and
                row.sensor_elevation is not None and
                row.sensor_elevation - nan_threshold < row.sensor_water_level_adj < row.sensor_elevation + nan_threshold
            ):
                row.sensor_water_level_adj = None  # set to None instead of np.nan for compatibility
                row.road_water_level_adj = None    # set to None instead of np.nan for compatibility
    
    return qresults


def write_survey(db: Session, data: schemas.add_survey):
    values = data.dict()

    string_date = values["date_surveyed"]
    values["date_surveyed"] = datetime.strptime(string_date, '%Y%m%d%H%M%S')

    new_survey = models.sensor_surveys(**values)
    new_survey.sensor_ID = new_survey.sensor_ID.strip()
    new_survey.place = new_survey.place.strip()

    record_in_db = db.query(models.sensor_surveys).filter(and_(
        models.sensor_surveys.date_surveyed == new_survey.date_surveyed,
        models.sensor_surveys.sensor_ID == new_survey.sensor_ID,
        models.sensor_surveys.place == new_survey.place
    )).all()

    if len(record_in_db) > 0:
        return "Record already in database. Measurement not written"

    if len(record_in_db) == 0:
        db.add(new_survey)
        db.commit()
        db.refresh(new_survey)

        f = open("/data-api-log/surveys_added.txt", "a")
        header = "date_added;place;sensor_ID;date_surveyed"
        f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ";" + str(new_survey) + "\n")
        f.close()

        return "SUCCESS! Record written to database"

def get_latest_ml_camera_data(db: Session, file_id: str):
    return db.query(models.ml_camera_data).filter(models.ml_camera_data.file_id == file_id).order_by(
        desc('date')).first()

def get_ml_camera_data(db: Session, min_date: datetime, max_date: datetime, file_id: str):
    return db.query(models.ml_camera_data).filter(and_(
        models.ml_camera_data.file_id == file_id,
        models.ml_camera_data.date >= min_date,
        models.ml_camera_data.date <= max_date
    )).order_by(asc('date')).all()

def write_new_ml_camera_data(db: Session, data: schemas.ml_camera_data_ingest):
    if ('floodstatus' not in data.body):
        return "Error: floodstatus missing from body field"
    
    if ('temperature' not in data.body):
        print("Temperature missing from request")
        return "Error: temperature missing from body field"
    
    when = datetime.fromtimestamp(int(data.when))
    new_data = models.ml_camera_data(file_id=data.file, date=when, flood_status=data.body['floodstatus'], temperature=data.body['temperature'])

    record_in_db = db.query(models.ml_camera_data).filter(and_(
        models.ml_camera_data.date == new_data.date,
        models.ml_camera_data.file_id == new_data.file_id,
    )).all()

    if len(record_in_db) > 0:
        return "Record already in database. Measurement not written"
    
    db.add(new_data)
    db.commit()

    return "SUCCESS! Record written to database"