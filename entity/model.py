from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List, Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Address(BaseModel):
    city: str
    country: str
    pin: str


class Socials(BaseModel):
    type: str
    url: HttpUrl


class StudentBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Student(StudentBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(..., min_length=3, max_length=50, frozen=True)
    last_name: str = Field(..., min_length=3, max_length=50, frozen=True)
    age: int = Field(..., gt=0)
    address: Address
    social: Socials
    email: List[EmailStr]


class UpdateStudent(StudentBaseModel):
    first_name: Optional[str] = Field(..., min_length=3, max_length=50, frozen=True)
    first_name: Optional[str] = Field(..., min_length=3, max_length=50, frozen=True)
    last_name: Optional[str] = Field(..., min_length=3, max_length=50, frozen=True)
    age: Optional[int] = Field(..., gt=0)
    address: Optional[Address]
    social: Optional[Socials]
    email: Optional[List[str]]
