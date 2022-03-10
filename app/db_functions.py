from sqlalchemy import desc, and_
from sqlalchemy.orm import Session

from app import models, schemas
# import arrow
# from dateutil import tz


def get_latest_measurement(db: Session, sensor_ID: str):
    return db.query(models.sensor_data).filter(models.sensor_data.sensor_ID == sensor_ID).order_by(
        desc('date')).first()


def write_new_measurements(db: Session, data: schemas.sensor_data_ingest):
    values = data.dict()
    del values["timezone"]

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

        return "SUCCESS! Record written to database"