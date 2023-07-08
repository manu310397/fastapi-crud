from fastapi import status, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from typing import List

from config.db import client
from entity.model import Student, UpdateStudent

student_route = APIRouter()

db = client.librarymanagement


@student_route.post("/", response_description="Create Student", response_model=Student)
async def save(student: Student):
    student = jsonable_encoder(student)
    new_student = await db.students.insert_one(student)
    created_student = await db.students.find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@student_route.get("/", response_description="List students", response_model=List[Student])
async def list_students():
    students = await db.students.find().to_list(1000)
    return students


@student_route.get('/{id}', response_description='Get a single student', response_model=Student)
async def get(id: str):
    student = await db.students.find_one({"_id": id})

    print(student)

    if student is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} is not found")


@student_route.put('/{id}', response_description='Update a student', response_model=Student)
async def update(id: str, student: UpdateStudent):
    update_student = {}

    existing_student = await db.students.find_one({"_id": id})
    if existing_student is None:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")

    for key, value in student.dict().items():
        if value is not None:
            update_student[key] = value

    result = await db.students.update_one({"_id": id}, {"$set": update_student})

    if result.modified_count == 1:
        updated_student = await db.students.find_one({"_id": id})
        if updated_student is not None:
            return updated_student
    else:
        return existing_student


@student_route.delete('/{id}', response_description='Delete a student')
async def delete(id: str):
    result = await db.students.delete_one({"_id": id})

    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@student_route.delete('/', response_description="Delete all students")
async def delete_all():
    result = await db.students.delete_many({})

    if result.acknowledged:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
