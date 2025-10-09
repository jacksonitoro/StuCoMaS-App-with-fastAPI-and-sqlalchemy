from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sprint2.models import Student, Instructor, Course, Enrollment


# ============================================================
# 🎓 STUDENT FEATURES
# ============================================================

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


def search_students(db: Session, query: str):
    """Search students by name or email."""
    return db.query(Student).filter(
        (Student.first_name.ilike(f"%{query}%")) |
        (Student.last_name.ilike(f"%{query}%")) |
        (Student.email.ilike(f"%{query}%"))
    ).all()


def get_student_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}


def get_student_grades(db: Session, student_id: int):
    enrollments = db.query(Enrollment).filter_by(student_id=student_id).all()
    return [{"course": e.course.title, "grade": e.grade} for e in enrollments]


# ============================================================
# 👩‍🏫 INSTRUCTOR FEATURES
# ============================================================

def create_instructor(db: Session, first_name: str, last_name: str, email: str, department: str):
    if db.query(Instructor).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Instructor with this email already exists.")
    instructor = Instructor(first_name=first_name, last_name=last_name, email=email, department=department)
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor


def get_courses_by_instructor(db: Session, instructor_id: int):
    return (
        db.query(Course)
        .filter(Course.instructor_id == instructor_id)
        .order_by(Course.title.asc())
        .all()
    )


def get_students_in_course(db: Session, course_id: int):
    """Return all students in a course, sorted alphabetically by first name."""
    enrollments = (
        db.query(Enrollment)
        .join(Student)
        .filter(Enrollment.course_id == course_id)
        .options(joinedload(Enrollment.student))
        .order_by(Student.first_name.asc(), Student.id.asc())
        .all()
    )
    students = [e.student for e in enrollments]
    return students


def assign_grade_by_instructor(db: Session, instructor_id: int, student_id: int, course_id: int, grade: int):
    course = db.query(Course).filter_by(id=course_id, instructor_id=instructor_id).first()
    if not course:
        raise HTTPException(status_code=403, detail="Instructor not authorized for this course.")
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Student not enrolled in this course.")
    enrollment.grade = grade
    db.commit()
    db.refresh(enrollment)
    return enrollment


# ============================================================
# 🧑‍💼 ADMIN FEATURES
# ============================================================

def get_all_enrollments(db: Session):
    """Return all enrollments with related student and course info."""
    db.commit()
    db.expire_all()

    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
        .all()
    )

    if not enrollments:
        db.commit()
        enrollments = (
            db.query(Enrollment)
            .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
            .all()
        )

    return enrollments


def assign_grade_by_admin(db: Session, student_id: int, course_id: int, grade: int):
    """Admin assigns or updates a grade. Creates enrollment if missing."""
    enrollment = db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()

    if not enrollment:
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

    enrollment.grade = grade
    db.commit()
    db.refresh(enrollment)
    return enrollment


# ============================================================
# 📘 COURSE FEATURES
# ============================================================

def create_course(db: Session, code: str, title: str, credits: int, instructor_id: int):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found.")
    course = Course(code=code, title=title, credits=credits, instructor_id=instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def search_courses(db: Session, query: str):
    return db.query(Course).filter(
        (Course.code.ilike(f"%{query}%")) |
        (Course.title.ilike(f"%{query}%"))
    ).all()


# ============================================================
# 🧾 ENROLLMENTS
# ============================================================

def enroll_student(db: Session, student_id: int, course_id: int):
    if db.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first():
        raise HTTPException(status_code=400, detail="Already enrolled.")
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
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
