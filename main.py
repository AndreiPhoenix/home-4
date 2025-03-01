from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from models import Base, Student
from crud import StudentDatabase
from database import init_db  # Импортируем init_db из database.py

app = FastAPI()

# Инициализация базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
SessionLocal = init_db(DATABASE_URL)

db = StudentDatabase()
db.init(SessionLocal)

@app.post("/load-data/")
def load_data(file_path: str):
    db.load_data_from_csv(file_path)
    return {"message": "Data successfully loaded from CSV"}

@app.get("/students/{faculty_name}")
def get_students(faculty_name: str):
    return db.get_students_by_faculty(faculty_name)

@app.get("/courses/")
def get_courses():
    return db.get_unique_courses()

@app.get("/avg-grade/{faculty_name}")
def get_avg_grade(faculty_name: str):
    return {"average_grade": db.get_average_grade_by_faculty(faculty_name)}

@app.post("/students/")
def create_student(last_name: str, first_name: str, faculty: str, course: str, grade: int):
    student = db.create_student(last_name, first_name, faculty, course, grade)
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, last_name: str, first_name: str, faculty: str, course: str, grade: int):
    student = db.update_student(student_id, last_name, first_name, faculty, course, grade)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = db.delete_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
