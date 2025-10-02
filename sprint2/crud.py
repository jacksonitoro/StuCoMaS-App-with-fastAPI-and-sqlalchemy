from fastapi import HTTPException
from sqlalchemy.orm import Session
from sprint2.models import Student, Instructor, Course, Enrollment


# --- Students ---
def create_student(db: Session, first_name: str, last_name: str, email: str):
    existing = db.query(Student).filter_by(email=email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")
    student = Student(first_name=first_name, last_name=last_name, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_students(db: Session):
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student

def update_student(db: Session, student_id: int, data: dict):
    student = get_student_by_id(db, student_id)
    for key, value in data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}


# --- Instructors ---
def create_instructor(db: Session, first_name: str, last_name: str, email: str, department: str):
    existing = db.query(Instructor).filter_by(email=email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Instructor with this email already exists.")
    instructor = Instructor(first_name=first_name, last_name=last_name, email=email, department=department)
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor

def get_instructor_by_id(db: Session, instructor_id: int):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found.")
    return instructor

def update_instructor(db: Session, instructor_id: int, data: dict):
    instructor = get_instructor_by_id(db, instructor_id)
    for key, value in data.items():
        setattr(instructor, key, value)
    db.commit()
    db.refresh(instructor)
    return instructor

def delete_instructor(db: Session, instructor_id: int):
    instructor = get_instructor_by_id(db, instructor_id)
    db.delete(instructor)
    db.commit()
    return {"message": f"Instructor {instructor_id} deleted successfully"}


# --- Courses ---
def create_course(db: Session, code: str, title: str, credits: int, instructor_id: int):
    existing = db.query(Course).filter_by(code=code, instructor_id=instructor_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course already exists for this instructor")
    course = Course(code=code, title=title, credits=credits, instructor_id=instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_course_by_id(db: Session, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return course

def update_course(db: Session, course_id: int, data: dict):
    course = get_course_by_id(db, course_id)
    for key, value in data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course_id: int):
    course = get_course_by_id(db, course_id)
    db.delete(course)
    db.commit()
    return {"message": f"Course {course_id} deleted successfully"}


# --- Enrollments ---
def enroll_student(db: Session, student_id: int, course_id: int):
    existing = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course.")
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def assign_grade(db: Session, student_id: int, course_id: int, grade: str):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found.")

    if grade < 1 or grade > 5:
        raise HTTPException(status_code=400, detail="Grade must be between 1 (excellent) and 5 (fail).")

    enrollment.grade = grade
    db.commit()
    db.refresh(enrollment)
    return enrollment

def delete_enrollment(db: Session, student_id: int, course_id: int):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return {"message": f"Enrollment for student {student_id} in course {course_id} deleted successfully"}
