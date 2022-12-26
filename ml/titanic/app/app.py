from fastapi import FastAPI, Body
from enum import IntEnum, Enum
from joblib import load
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

classfier = load("./model/titanic.joblib")

app = FastAPI(
    title="Titanic ML API",
    description="API for titanic survive predictions",
    version="1.0",
)

# Enumerations
class PassengerClass(IntEnum):
    """Passenger Class
    1 Cl, 2 Cl, 3 Cl
    Args:
        IntEnum (int): Passenger Class
    """

    first = 1
    second = 2
    third = 3


class GenderClass(Enum):
    """Gender Selector

    Args:
        Enum (String): Gender of the person, choos between male and female
    """

    female = "female"
    male = "male"


class EmbarkedClass(Enum):
    """Embarked Class

    Args:
        Enum (string): Embarked Station
    """

    S = "S"
    C = "C"
    Q = "Q"


# Response Model
class PredictionResponse(BaseModel):
    passenger_class: int
    sex: int
    age: float
    sibsp: int
    parch: int
    fare: float
    embarked: int
    prediction: int
    log_proba: List


@app.get("/predict", tags=["predict"], response_model=PredictionResponse)
async def get_prediction(
    passenger_class: PassengerClass,
    sex: GenderClass,
    age: float,
    sibsp: int,
    parch: int,
    fare: float,
    embarked: EmbarkedClass,
) -> PredictionResponse:
    processed_sex = dict({"female": 0, "male": 1}).get(sex.value)
    processed_embarked = dict({"S": 3, "C": 2, "Q": 1}).get(embarked.value)
    prediction = classfier.predict(
        [
            [
                passenger_class.value,
                processed_sex,
                age,
                sibsp,
                parch,
                fare,
                processed_embarked,
            ]
        ]
    ).tolist()
    log_proba = classfier.predict_proba(
        [
            [
                passenger_class.value,
                processed_sex,
                age,
                sibsp,
                parch,
                fare,
                processed_embarked,
            ]
        ]
    ).tolist()

    return PredictionResponse(
        passenger_class=passenger_class.value,
        sex=processed_sex,
        age=age,
        sibsp=sibsp,
        parch=parch,
        fare=fare,
        embarked=processed_embarked,
        prediction=prediction[0],
        log_proba=log_proba,
    )
