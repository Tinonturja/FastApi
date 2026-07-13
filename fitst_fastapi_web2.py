from fastapi import FastAPI, Path, HTTPException
import json
from pydantic import BaseModel, Field
from typing import Annotated, List, Dict

class Patient_info(BaseModel):
    patient_id: Annotated[str, Field(description="Give the id of the patient")]
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

@app.get("/")
def home_function():
    return {'message': "Hello world"}

# view the patient data 
@app.get("/view")
def view_patient():
    data = load_data()
    return data
@app.get("/view/{patient_id}")
def get_patient(patient_id):
    data = load_data()
    patient_id_list = [id for id in data.keys()]
    if patient_id not in patient_id_list:
        raise HTTPException(f"Patient ID is not in the database. Submit the id within this list {patient_id_list}")
    
    return data[patient_id]



