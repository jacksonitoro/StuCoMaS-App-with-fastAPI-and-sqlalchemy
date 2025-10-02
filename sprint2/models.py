
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sprint2.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String)

    courses = relationship("Course", back_populates="instructor")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    credits = Column(Integer, default=3)

    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    instructor = relationship("Instructor", back_populates="courses")

    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("code", "instructor_id", name="uq_course_instructor"),)

class Enrollment(Base):
    __tablename__ = "enrollments"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    grade = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 5", name="check_grade_range"),
    )

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
