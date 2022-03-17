import datetime
import secrets
import os

from app import models
from app import database
from app import db_functions
from app import schemas
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from datetime import datetime

# # Uncomment for working locally to access env vars
# from app import environment_vars
# environment_vars.set_env_vars()

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

security = HTTPBasic()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/get_latest_measurement')
def get_latest_measurement(
        sensor_ID: str,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    latest_measurement = db_functions.get_latest_measurement(db=db, sensor_ID=sensor_ID)

    return {
        latest_measurement
    }


@app.post('/write_measurement')
def write_measurement(
        data: schemas.sensor_data_ingest,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    response = db_functions.write_new_measurements(
        db=db,
        data=data
    )

    return {
        response
    }


@app.get('/get_water_level')
def get_water_level(
        min_date: str,
        max_date: str,
        sensor_ID: str,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    parsed_min_date = datetime.strptime(min_date, '%Y-%m-%d')
    parsed_max_date = datetime.strptime(max_date, '%Y-%m-%d')

    return db_functions.get_water_level(
        db=db,
        min_date=parsed_min_date,
        max_date=parsed_max_date,
        sensor_ID=sensor_ID
    )

@app.post('/add_survey')
def add_survey(
        data: schemas.add_survey,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return db_functions.write_survey(
        db=db,
        data=data
    )