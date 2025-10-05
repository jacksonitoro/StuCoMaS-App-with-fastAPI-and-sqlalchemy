from fastapi import HTTPException
from sqlalchemy.orm import Session
from sprint2.models import Student, Instructor, Course, Enrollment


# --- Search / Filter ---
def search_students(db: Session, query: str):
    return db.query(Student).filter(
        (Student.first_name.ilike(f"%{query}%")) |
        (Student.last_name.ilike(f"%{query}%")) |
        (Student.email.ilike(f"%{query}%"))
    ).all()


def search_courses(db: Session, query: str):
    return db.query(Course).filter(
        (Course.code.ilike(f"%{query}%")) |
        (Course.title.ilike(f"%{query}%"))
    ).all()


# --- Students ---
def create_student(db: Session, first_name: str, last_name: str, email: str):
    if db.query(Student).filter_by(email=email).first():
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


# --- Instructors ---
def create_instructor(db: Session, first_name: str, last_name: str, email: str, department: str):
    if db.query(Instructor).filter_by(email=email).first():
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


# --- Courses ---
def create_course(db: Session, code: str, title: str, credits: int, instructor_id: int):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found.")
    course = Course(code=code, title=title, credits=credits, instructor_id=instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    course.instructor = instructor
    return course


# --- Enrollments ---
def enroll_student(db: Session, student_id: int, course_id: int, grade: int = None):
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course not found.")

    existing = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course.")

    enrollment = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    enrollment.student = student
    enrollment.course = course
    return enrollment


def assign_grade(db: Session, student_id: int, course_id: int, grade: int):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found.")
    if grade < 1 or grade > 5:
        raise HTTPException(status_code=400, detail="Grade must be between 1 and 5.")
    enrollment.grade = grade
    db.commit()
    db.refresh(enrollment)
    return enrollment
