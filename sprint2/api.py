
from fastapi import FastAPI, Depends, HTTPException
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
    return crud.create_student(db, **student.model_dump())

@app.get("/students/", response_model=list[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get("/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.model_dump().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}


# --- Instructors ---
@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, **instructor.model_dump())


# --- Courses ---
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, **course.model_dump())


# --- Enrollments ---
@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, **enrollment.model_dump())
