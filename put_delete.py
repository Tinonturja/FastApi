from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal
from create_fastapi import load_data, Patient, save_data
class PatientUpdate(BaseModel):
    #id: Annotated[Optional[str], Field(default=None)] Part of the patient id--> so it got removed
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]

# Steps:
#1. Build new pydantic model 
#2. new data updates the existing data point
# edit has two endpoints 
#1. Patient.id --> Path parameter
#2. Request Body --> You describe what to change and how to change

router = APIRouter()
# Building the endpoint
@router.put("/edit/{patient_id}")
def update_patient_info(patient_id: str,
                        patient_update:PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="The id you have been searching for is not in the database")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True) # Get the data that set by the user: Example: The user only provide update value for City and Age, so the dictionary contain only those two values

    # updated_patient_info is a dict now, which has all the values, but not the id, and not the computed field
    updated_patient_info['id'] = patient_id
    # updated patient_info has all the necessary features & Turn it in a pydantic object
    patient_info = Patient(**updated_patient_info)
    # again convert the pydantic object in a dict
    full_patient_info = patient_info.model_dump() # creates the dict
    for key, value in full_patient_info.items():
        existing_patient_info[key] = value
    data[patient_id] = existing_patient_info # now existing patient info has all the updated value
   
    save_data(data)

    return JSONResponse(status_code= 200, content = "Successfully updated the patient")



    
