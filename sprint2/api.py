# sprint2/api.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sprint2.database import SessionLocal, engine, Base
import sprint2.crud as crud
import sprint2.models as models

# Create tables if not already present
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StuCoMaS API")

@app.get("/")
def root():
    return {"message": "Welcome to StuCoMaS API 🚀"}


# Dependency: provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- STUDENTS ---
@app.post("/students/")
def create_student(first_name: str, last_name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_student(db, first_name, last_name, email)

@app.get("/students/")
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


# --- INSTRUCTORS ---
@app.post("/instructors/")
def create_instructor(first_name: str, last_name: str, email: str, department: str, db: Session = Depends(get_db)):
    return crud.create_instructor(db, first_name, last_name, email, department)

@app.get("/instructors/")
def list_instructors(db: Session = Depends(get_db)):
    return db.query(models.Instructor).all()


# --- COURSES ---
@app.post("/courses/")
def create_course(code: str, title: str, credit_hours: int, instructor_id: int, db: Session = Depends(get_db)):
    return crud.create_course(db, code, title, credit_hours, instructor_id)

@app.get("/courses/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


# --- ENROLLMENTS ---
@app.post("/enrollments/")
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return crud.enroll_student(db, student_id, course_id)

@app.post("/grades/")
def assign_grade(student_id: int, course_id: int, grade: str, db: Session = Depends(get_db)):
    return crud.assign_grade(db, student_id, course_id, grade)
