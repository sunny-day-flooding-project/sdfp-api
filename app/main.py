import secrets
import os

from app import models
from app import database
from app import db_functions
from app import schemas
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

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


@app.get('/get_latest_measurement')
async def get_latest_measurement(
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
async def write_measurement(
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