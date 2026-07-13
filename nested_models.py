from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_dict = {'city': 'Mymensingh', 'state': 'Bangladesh', 'pin': '2200'}
add_obj = Address(**address_dict)

patient_dict = {'name': 'Tinon Turja', 'age': 26, 'address': add_obj}
patient_obj = Patient(**patient_dict)

print(patient_obj)
print(patient_obj.address.city)
print(patient_obj.address.state)
print(patient_obj.address.pin)

temp = patient_obj.model_dump()
print(temp)
temp2 = patient_obj.model_dump_json()
print(temp2)