from fastapi import FastAPI, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from sprint2.schemas import EnrollmentGradeUpdate
from sprint2.database import SessionLocal, Base, engine
from sprint2 import crud, models, schemas

# Create database tables (only for dev, not in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StuCoMaS API")


# --- Dependency: Database Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# 🧑‍🎓 STUDENT ROUTES
# ============================================================

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, **student.model_dump())


@app.get("/students/", response_model=List[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/search", response_model=List[schemas.Student])
def search_students(query: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_students(db, query)


@app.get("/students/{student_id}/grades", response_model=List[schemas.StudentGrade])
def get_student_grades(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_grades(db, student_id)


# ============================================================
# 👩‍🏫 INSTRUCTOR ROUTES
# ============================================================

@app.post("/instructors/", response_model=schemas.Instructor)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    return crud.create_instructor(db, **instructor.model_dump())


@app.get("/instructors/{instructor_id}/courses", response_model=List[schemas.Course])
def get_courses_by_instructor(instructor_id: int, db: Session = Depends(get_db)):
    return crud.get_courses_by_instructor(db, instructor_id)


@app.get("/instructors/{instructor_id}/courses/{course_id}/students", response_model=List[schemas.Student])
def get_students_in_course(instructor_id: int, course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.id == course_id,
        models.Course.instructor_id == instructor_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found or unauthorized")

    return [enrollment.student for enrollment in course.enrollments]


@app.put("/instructors/{instructor_id}/courses/{course_id}/students/{student_id}/grade")
def assign_grade_instructor(
    instructor_id: int,
    course_id: int,
    student_id: int,
    grade: int,
    db: Session = Depends(get_db),
    x_role: Optional[str] = Header(None)
):
    # Simple RBAC check (for tests)
    if x_role and x_role.lower() != "instructor":
        raise HTTPException(status_code=403, detail="Forbidden: Only instructors can assign grades")

    course = db.query(models.Course).filter(
        models.Course.id == course_id,
        models.Course.instructor_id == instructor_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found or unauthorized")

    return crud.assign_grade(db, student_id, course_id, grade)


# ============================================================
# 🧑‍💼 ADMIN ROUTES
# ============================================================

@app.get("/admin/enrollments", response_model=List[schemas.Enrollment])
def get_all_enrollments(db: Session = Depends(get_db)):
    return crud.get_all_enrollments(db)



@app.put("/admin/students/{student_id}/courses/{course_id}/grade")
def admin_assign_grade(student_id: int, course_id: int, grade: int = Query(...), db: Session = Depends(get_db)):
    """Admin assigns or updates a grade."""
    return crud.assign_grade_by_admin(db, student_id, course_id, grade)




# ============================================================
# 📘 COURSE & ENROLLMENT ROUTES
# ============================================================

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, **course.model_dump())


@app.get("/courses/search", response_model=List[schemas.Course])
def search_courses(query: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_courses(db, query)


@app.post("/enrollments/", response_model=schemas.Enrollment)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Filter out grade since it's optional in EnrollmentCreate
    data = {k: v for k, v in enrollment.model_dump().items() if k != "grade"}
    return crud.enroll_student(db, **data)


@app.put("/enrollments/{student_id}/{course_id}/grade", response_model=schemas.Enrollment)
def assign_grade(student_id: int, course_id: int, payload: EnrollmentGradeUpdate, db: Session = Depends(get_db)):
    return crud.assign_grade(db, student_id, course_id, payload.grade)
