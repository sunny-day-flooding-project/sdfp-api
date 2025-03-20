import datetime
import secrets
import os

from app import models
from app import database
from app import db_functions
from app import schemas
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# # Uncomment for working locally to access env vars
# from app import environment_vars
# environment_vars.set_env_vars()

models.database.Base.metadata.create_all(bind=database.engine)

description = """
Sunny Day Flooding Project Data API lets you:

* **Write pressure data**
* **Read water level data**
* **Add survey data**
* **Read survey data**
"""

app = FastAPI(
    title="Sunny Day Flooding Project Data API",
    description=description,
    version="0.1.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ian Hoyt",
        "url": "https://tarheels.live/sunnydayflood/people/",
        "email": "ianiac@email.unc.edu",
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)

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
        sensor_ID: str = Query(..., description="Example: BF_01"),
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
        min_date: str = Query(..., description="Example: 2022-01-01. Date format is '%Y-%m-%d'"),
        max_date: str = Query(..., description="Example: 2022-01-03. Date format is '%Y-%m-%d'"),
        sensor_ID: str = Query(..., description="Example: BF_01"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))
    ro_username2 = secrets.compare_digest(credentials.username, os.environ.get('ro_username2'))
    ro_password2 = secrets.compare_digest(credentials.password, os.environ.get('ro_password2'))

    if not ((correct_username and correct_password) or (ro_username and ro_password) or (ro_username2 and ro_password2)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    parsed_min_date = datetime.strptime(min_date, '%Y-%m-%d')
    parsed_max_date = datetime.strptime(max_date, '%Y-%m-%d')

    if(parsed_max_date < parsed_min_date):
        raise HTTPException(status_code=400, detail="Max date is before Min date")

    if((parsed_max_date - parsed_min_date) > timedelta(days=30)):
        raise HTTPException(status_code=400, detail="Date range is greater than 30 days. Please decrease date range to seven days or less. Sincerely, 🤖. Beep beep boop")

    return db_functions.get_water_level(
        db=db,
        min_date=parsed_min_date,
        max_date=parsed_max_date,
        sensor_ID=sensor_ID
    )

@app.post('/write_survey')
def write_survey(
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

@app.get('/get_surveys')
def get_surveys(
        sensor_ID: str = Query("all", description="Example: BF_01"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))
    ro_username2 = secrets.compare_digest(credentials.username, os.environ.get('ro_username2'))
    ro_password2 = secrets.compare_digest(credentials.password, os.environ.get('ro_password2'))

    if not ((correct_username and correct_password) or (ro_username and ro_password) or (ro_username2 and ro_password2)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    sensor_ID = sensor_ID.strip()

    if sensor_ID == "all":
        return db_functions.get_all_surveys(
            db=db
        )

    return db_functions.get_surveys(
        db=db,
        sensor_ID=sensor_ID
    )

@app.post('/write_ml_camera_data')
def write_ml_camera_data(
        data: schemas.ml_camera_data_ingest,
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
    
    response = db_functions.write_new_ml_camera_data(
        db=db,
        data=data
    )

    return {
        response
    }

@app.get('/get_latest_ml_camera_data')
def get_latest_ml_camera_data(
        file_id: str = Query(..., description="Example: 2037335832365003001c00c8#camera002.qo"),
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

    latest_data = db_functions.get_latest_ml_camera_data(db=db, file_id=file_id)

    return {
        latest_data
    }

@app.get('/get_ml_camera_data')
def get_ml_camera_data(
        file_id: str = Query(..., description="Example: 2037335832365003001c00c8#camera002.qo"),
        min_date: str = Query(..., description="Example: 2022-01-01. Date format is '%Y-%m-%d'"),
        max_date: str = Query(..., description="Example: 2022-01-03. Date format is '%Y-%m-%d'"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not ((correct_username and correct_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    parsed_min_date = datetime.strptime(min_date, '%Y-%m-%d')
    parsed_max_date = datetime.strptime(max_date, '%Y-%m-%d')

    if(parsed_max_date < parsed_min_date):
        raise HTTPException(status_code=400, detail="Max date is before Min date")

    if((parsed_max_date - parsed_min_date) > timedelta(days=7)):
        raise HTTPException(status_code=400, detail="Date range is greater than 7 days. Please decrease date range to seven days or less.")
    
    return db_functions.get_ml_camera_data(
        db=db,
        min_date=parsed_min_date,
        max_date=parsed_max_date,
        file_id=file_id
    )

@app.get('/get_api_data')
def get_api_data(
        id: str = Query(..., description="Example: 8656483"),
        api_name: str = Query(..., description="Example: NOAA"),
        type: str = Query(..., description="Example: water_level"),
        min_date: str = Query(..., description="Example: 2022-01-01. Date format is '%Y-%m-%d'"),
        max_date: str = Query(..., description="Example: 2022-01-03. Date format is '%Y-%m-%d'"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))
    ro_username2 = secrets.compare_digest(credentials.username, os.environ.get('ro_username2'))
    ro_password2 = secrets.compare_digest(credentials.password, os.environ.get('ro_password2'))

    if not ((correct_username and correct_password) or (ro_username and ro_password) or (ro_username2 and ro_password2)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    parsed_min_date = datetime.strptime(min_date, '%Y-%m-%d')
    parsed_max_date = datetime.strptime(max_date, '%Y-%m-%d')

    if(parsed_max_date < parsed_min_date):
        raise HTTPException(status_code=400, detail="Max date is before Min date")

    if((parsed_max_date - parsed_min_date) > timedelta(days=7)):
        raise HTTPException(status_code=400, detail="Date range is greater than 7 days. Please decrease date range to seven days or less.")

    return db_functions.get_api_data(
        db=db,
        min_date=parsed_min_date,
        max_date=parsed_max_date,
        id=id,
        type=type,
        api_name=api_name,
    )