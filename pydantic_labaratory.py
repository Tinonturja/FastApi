from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    age: int
    school_name: str

student_info = {'name': "Turja", "age":19,"school_name": "mzs"}
student_obj = Student(**student_info)

def print_student_info(student: Student):
    print(student.name)
    print(student.age)
    print(student.school_name)

print_student_info(student_obj)