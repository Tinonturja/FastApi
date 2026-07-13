from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator,computed_field
from typing import List, Dict, Optional, Annotated

# field validator is used to validate the data field, and only one at a time
# To validate multiple fields at once, we can use the model validator, which is used to validate the entire model

class Patient(BaseModel):
    name: Annotated[str, Field(max_length= 50, title = "Patient Name", description = "Give me the name of the patient")]
    email: Annotated[str, Field(description = "The email address of the patient")]
    age: int = Field(gt = 0, description = "The age of the patient")
    weight: float = Field(gt = 0, strict = True, description = "The weight of the patient") #kg
    height: Annotated[float, Field(gt =0, strict = True, description = "The height of the patient")] #mtr
    married: Annotated[bool, Field(default = False,description = "Whether the patient is married")] # optional field, can be None
    #bmi: Annotated[float | None, Field(default = None, description = "The BMI of the patient")] = None
    allergies: Annotated[Optional[List[str]], Field(default = [], description = "List of allergies of the patient")] # optional field, can be None
    contact_details: Dict[str, str]

# check the mail address for a specific group
    @field_validator('email') # on which data field we want to apply the validation
    @classmethod
    def validate_email(cls, value): # cls is given, as if there any other class method, we can use it in the validation
        valid_domains = ['brac.net', 'gmail.com', 'yahoo.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        return value.upper() # convert the name to uppercase
    
    @model_validator(mode = 'after') # after the model is created, we can validate the entire model
    def validate_emergency_contact(cls, model):
        required_fields = ['EMERGENCY', 'CONTACT']
        if model.age > 60 and not any(field.lower() in model.contact_details for field in required_fields):
            raise ValueError("Emergency contact is required for patients above 60 years old")
        return model
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height ** 2), 2)


def update_patient_data(patientinfo: Patient):
    print(f"Name: {patientinfo.name}")
    print(f"Email: {patientinfo.email}")
    print(f"Age: {patientinfo.age}")
    print(f"Weight: {patientinfo.weight}")
    print(f"Married: {patientinfo.married}")
    print(f"BMI: {patientinfo.bmi}")
    print(f"Allergies: {patientinfo.allergies}")
    print(f"Contact Details: {patientinfo.contact_details}")

patient_info = {'name': 'tinon turja', 'email': 'john.doe@gmail.com', 'age': 65, 'weight': 70.5, 'height': 1.75, 'allergies': ['pollen', 'dust'], 'contact_details': {'emergency':'+8801711669374','phone': '123-456-7890'}}
patient = Patient(**patient_info)
update_patient_data(patient)