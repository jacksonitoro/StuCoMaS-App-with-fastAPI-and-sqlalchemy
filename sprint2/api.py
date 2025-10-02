from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sprint2 import crud, models, schemas
from sprint2.database import SessionLocal, engine
from sprint2.schemas import EnrollmentGradeUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StuCoMaS API 🚀")

# Dependency
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
    return crud.get_student_by_id(db, student_id)

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.update_student(db, student_id, student.model_dump())

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return crud.delete_student(db, student_id)


# --- Instructors ---
@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, **instructor.model_dump())

@app.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    return crud.get_instructor_by_id(db, instructor_id)

@app.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int, instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.update_instructor(db, instructor_id, instructor.model_dump())

@app.delete("/instructors/{instructor_id}")
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    return crud.delete_instructor(db, instructor_id)


# --- Courses ---
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, **course.model_dump())

@app.get("/courses/{course_id}", response_model=schemas.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return crud.get_course_by_id(db, course_id)

@app.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.update_course(db, course_id, course.model_dump())

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return crud.delete_course(db, course_id)


# --- Enrollments ---
@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, **enrollment.model_dump())

@app.put("/enrollments/{student_id}/{course_id}/grade", response_model=schemas.Enrollment)
def update_enrollment_grade(
    student_id: int,
    course_id: int,
    grade_update: EnrollmentGradeUpdate,
    db: Session = Depends(get_db),
):
    return crud.assign_grade(db, student_id, course_id, grade_update.grade)

@app.delete("/enrollments/{student_id}/{course_id}")
def delete_enrollment(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return crud.delete_enrollment(db, student_id, course_id)
