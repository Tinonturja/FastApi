from fastapi import FastAPI, Path, HTTPException, Query
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

@app.get("/specificview/{patient_id}")
def specific_view(patient_id: str = Path(..., description = "The specific patient id to view the data")):
    data = load_data()
    patient_id_list = [id for id in data.keys()]
    if patient_id not in patient_id_list:
        raise HTTPException(status_code = 404, detail = f"Patient ID is not in the database. Submit the id within this list {patient_id_list}")
    
    return data[patient_id]

@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description = "The criteria to sort by: height, weight, and bmi"),
                 order_by: str = Query('asc', description = "The order to sort by: asc or desc") ):
    data = load_data()
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"The data should be sory by the following fields: {valid_fields}")
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail= "order should follow two method: either ascending or descending")
    reverse_option = True if order_by == 'desc' else False
    data = sorted(data.values(), key = lambda x: x.get(sort_by,0), reverse= reverse_option)

    return data
