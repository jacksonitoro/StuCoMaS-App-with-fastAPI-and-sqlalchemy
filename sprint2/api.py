from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sprint2 import crud, models, schemas
from sprint2.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StuCoMaS API 🚀")

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Root ---
@app.get("/")
def read_root():
    return {"message": "Welcome to StuCoMaS API 🚀"}


# --- Students ---
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, **student.dict())

@app.get("/students/", response_model=list[schemas.Student])  # ✅ use modern style
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get("/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_by_id(db, student_id)


# --- Instructors ---
@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, **instructor.dict())


# --- Courses ---
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, **course.dict())


# --- Enrollments ---
@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, **enrollment.dict())
