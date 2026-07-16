from fastapi import FastAPI, Path, HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

router = APIRouter()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the Patient", examples=["P001", "P002"])]
    name: Annotated[str, Field(..., description="name of the patient", max_length=50)]
    city: Annotated[str, Field(..., description="The city where the patient currently live")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the Patient")]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender of the Patient")]
    height: Annotated[float, Field(..., description="The height of the patient in mtrs")]
    weight: Annotated[float, Field(..., description="The weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi > 25:
            return "Obese"
        return "Unknown"


def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)


@router.get("/")
def welcome_patient_management_system():
    return {"message": "Welcome to Patient Management System"}


@router.get("/hello")
def hello():
    return {"message": "Patient management system api."}


@router.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records."}


@router.get("/creator")
def creator():
    return {"message": "This application was created by Tinon Turja Majumder."}


@router.get("/view")
def view():
    data = load_data()
    return data


@router.get("/view/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {"error": "Patient not found."}


@router.get("/specificview/{patient_id}")
def specific_view(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples=["P001"])):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found.")


@router.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, and bmi"),
    order_by: str = Query("asc", description="Sort in ascending or descending order"),
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Should be selected from {valid_fields}")
    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Order either be asc or desc")

    data = load_data()
    order_stat = True if order_by == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=order_stat)

    return sorted_data


@router.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient Created successfully"})
