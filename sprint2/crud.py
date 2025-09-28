from sqlalchemy.orm import Session
from sprint2.models import Student, Instructor, Course, Enrollment


# --- Students ---
def create_student(db: Session, first_name: str, last_name: str, email: str):
    existing = db.query(Student).filter_by(email=email).first()
    if existing:
        return existing

    student = Student(first_name=first_name, last_name=last_name, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


# --- Instructors ---
def create_instructor(db: Session, first_name: str, last_name: str, email: str, department: str):
    existing = db.query(Instructor).filter_by(email=email).first()
    if existing:
        return existing

    instructor = Instructor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        department=department
    )
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor


# --- Courses ---
def create_course(db: Session, code: str, title: str, credit_hours: int, instructor_id: int):
    existing = db.query(Course).filter_by(code=code, instructor_id=instructor_id).first()
    if existing:
        return existing

    course = Course(code=code, title=title, credits=credit_hours, instructor_id=instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


# --- Enrollments ---
def enroll_student(db: Session, student_id: int, course_id: int):
    existing = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        return existing

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def assign_grade(db: Session, student_id: int, course_id: int, grade: str):
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if enrollment:
        enrollment.grade = grade
        db.commit()
        db.refresh(enrollment)
    return enrollment
