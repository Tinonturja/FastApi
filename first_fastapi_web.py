import json

from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()
def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)

    return data

@app.get("/") # get request to the root endpoint
def hello():
    return {"message": "Patient management system api."}

@app.get('/about')
def about():
    return {"message": "A fully functional API to manage your patient records."}  

@app.get('/creator')
def creator():
    return {"message": "This application was created by Tinon Turja Majumder."}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/view/{patient_id}')
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {"error": "Patient not found."}

# patient id with proper definition and description
@app.get('/specificview/{patient_id}')
def specific_view(patient_id: str = Path(..., description = "The ID of the patient to retrieve", example = "P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "Patient not found.")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description= "Sort on the basis of height, weight, and bmi"),
                  order_by: str = Query('asc', description="Sort in ascending or descending order")):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = f"Invalid field. Should be selected from {valid_fields}")
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail = "Invalid order. Order either be asc or desc")

    data = load_data()
    order_stat = True if order_by == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by,0), reverse = order_stat)

    return sorted_data
