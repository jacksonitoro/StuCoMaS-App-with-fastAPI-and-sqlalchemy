from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sprint2.database import SessionLocal, engine, Base
import sprint2.crud as crud
import sprint2.models as models
import sprint2.schemas as schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StuCoMaS API")


# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Root ---
@app.get("/")
def root():
    return {"message": "Welcome to StuCoMaS API 🚀"}


# --- STUDENTS ---
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student.first_name, student.last_name, student.email)

@app.get("/students/", response_model=list[schemas.Student])
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


# --- INSTRUCTORS ---
@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(
        db,
        instructor.first_name,
        instructor.last_name,
        instructor.email,
        instructor.department
    )

@app.get("/instructors/", response_model=list[schemas.Instructor])
def list_instructors(db: Session = Depends(get_db)):
    return db.query(models.Instructor).all()


# --- COURSES ---
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course.code, course.title, course.credit_hours, course.instructor_id)

@app.get("/courses/", response_model=list[schemas.Course])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


# --- ENROLLMENTS ---
@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, enrollment.student_id, enrollment.course_id)

@app.post("/grades/", response_model=schemas.Enrollment)
def assign_grade(student_id: int, course_id: int, grade: str, db: Session = Depends(get_db)):
    return crud.assign_grade(db, student_id, course_id, grade)
