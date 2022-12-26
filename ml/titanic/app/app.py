from fastapi import FastAPI, Body
from enum import IntEnum, Enum
from joblib import load
from fastapi.responses import JSONResponse

classfier = load("./model/titanic.joblib")

app = FastAPI(
    title="Titanic ML API",
    description="API for titanic survive predictions",
    version="1.0",
)

# Enumerations
class PassengerClass(IntEnum):
    first = 1
    second = 2
    third = 3


class GenderClass(Enum):
    female = "female"
    male = "male"


class EmbarkedClass(Enum):
    S = "S"
    C = "C"
    Q = "Q"


# Pclass	Sex	Age	SibSp	Parch	Fare	Embarked
@app.get("/predict", tags=["predict"])
async def get_prediction(
    passenger_class: PassengerClass,
    sex: GenderClass,
    age: float,
    sibsp: int,
    parch: int,
    fare: float,
    embarked: EmbarkedClass,
):
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

    return JSONResponse(
        {
            "PassengerClass": passenger_class.value,
            "sex": processed_sex,
            "age": age,
            "sibsp": sibsp,
            "parch": parch,
            "fare": fare,
            "embarked": processed_embarked,
            "prediction": prediction[0],
            "log_proba": log_proba,
        }
    )
