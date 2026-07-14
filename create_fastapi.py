from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, model_validator, Field,computed_field
from typing import Optional, List, Dict, Annotated, Literal
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description= "ID of the Patient", examples=['P001', 'P002'])]
    name: Annotated[str, Field(..., description="name of the patient", max_length=50) ]
    city: Annotated[str, Field(..., description="The city where the patient currently live")]
    age: Annotated[int, Field(..., gt = 0,lt = 120, description="Age of the Patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description = "Gender of the Patient")]
    height: Annotated[float, Field(..., description="The height of the patient in mtrs")]
    weight: Annotated[float, Field(..., description="The weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi>25:
            return "Obese"
        
def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file)

@app.get("/")
def welcome_patient_management_system():
    return {'message': 'Welcome to Patient Management System'}

# create the api endpoint
@app.post("/create")
def create_patient(patient: Patient):

    # load the data
    data = load_data()
    # check if the data exists or not
    if patient.id in data:
        raise HTTPException(status_code= 400, detail= "Patient already exists")
    
    # save the data into the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content = {'message': 'Patient Created successfully'})
