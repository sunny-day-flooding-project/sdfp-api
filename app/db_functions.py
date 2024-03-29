from sqlalchemy import desc, and_
from sqlalchemy.orm import Session

from app import models, schemas
from datetime import datetime, timezone


def get_latest_measurement(db: Session, sensor_ID: str):
    return db.query(models.sensor_data).filter(models.sensor_data.sensor_ID == sensor_ID).order_by(
        desc('date')).first()


def get_surveys(db: Session, sensor_ID: str):
    return db.query(models.sensor_surveys).filter(models.sensor_surveys.sensor_ID == sensor_ID).order_by(
        desc('date_surveyed')).all()


def get_all_surveys(db: Session):
    return db.query(models.sensor_surveys).order_by(
        desc('date_surveyed')).all()


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


def get_water_level(db: Session, min_date: datetime, max_date: datetime, sensor_ID: str):
    return db.query(models.data_for_display).filter(and_(
        models.data_for_display.date >= min_date,
        models.data_for_display.date <= max_date,
        models.data_for_display.sensor_ID == sensor_ID
    )).all()


def write_survey(db: Session, data: schemas.add_survey):
    values = data.dict()

    string_date = values["date_surveyed"]
    values["date_surveyed"] = datetime.strptime(string_date, '%Y%m%d%H%M%S')

    new_survey = models.sensor_surveys(**values)

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
