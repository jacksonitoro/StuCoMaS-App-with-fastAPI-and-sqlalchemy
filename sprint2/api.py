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
    return crud.create_student(db, **student.dict())

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
def update_student(student_id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updated.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


# --- Instructors ---
@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, **instructor.dict())

@app.get("/instructors/", response_model=list[schemas.Instructor])
def get_instructors(db: Session = Depends(get_db)):
    return db.query(models.Instructor).all()

@app.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@app.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int, updated: schemas.InstructorCreate, db: Session = Depends(get_db)):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    for key, value in updated.dict().items():
        setattr(instructor, key, value)
    db.commit()
    db.refresh(instructor)
    return instructor

@app.delete("/instructors/{instructor_id}")
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    db.delete(instructor)
    db.commit()
    return {"message": "Instructor deleted successfully"}


# --- Courses ---
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, **course.dict())

@app.get("/courses/", response_model=list[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@app.get("/courses/{course_id}", response_model=schemas.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, updated: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in updated.dict().items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}


# --- Enrollments ---
@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, **enrollment.dict())

@app.get("/enrollments/", response_model=list[schemas.Enrollment])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

@app.get("/enrollments/{student_id}/{course_id}", response_model=schemas.Enrollment)
def get_enrollment(student_id: int, course_id: int, db: Session = Depends(get_db)):
    enrollment = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.student_id == student_id,
                models.Enrollment.course_id == course_id)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@app.put("/enrollments/{student_id}/{course_id}", response_model=schemas.Enrollment)
def update_enrollment(student_id: int, course_id: int, updated: schemas.EnrollmentBase, db: Session = Depends(get_db)):
    enrollment = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.student_id == student_id,
                models.Enrollment.course_id == course_id)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.grade = updated.grade
    db.commit()
    db.refresh(enrollment)
    return enrollment

@app.delete("/enrollments/{student_id}/{course_id}")
def delete_enrollment(student_id: int, course_id: int, db: Session = Depends(get_db)):
    enrollment = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.student_id == student_id,
                models.Enrollment.course_id == course_id)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}
