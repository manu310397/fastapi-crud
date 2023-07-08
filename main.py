from fastapi import FastAPI

from routes.student_route import student_route

app = FastAPI()
app.include_router(student_route)
