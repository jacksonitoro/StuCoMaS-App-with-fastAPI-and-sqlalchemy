
from pydantic import BaseModel, EmailStr
from typing import Optional, List


# --- Student ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


# --- Instructor ---
class InstructorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: Optional[str] = None


class InstructorCreate(InstructorBase):
    pass


class Instructor(InstructorBase):
    id: int

    class Config:
        orm_mode = True


# --- Course ---
class CourseBase(BaseModel):
    code: str
    title: str
    credit_hours: int


class CourseCreate(CourseBase):
    instructor_id: int


class Course(CourseBase):
    id: int
    instructor_id: Optional[int]

    class Config:
        orm_mode = True


# --- Enrollment ---
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    class Config:
        orm_mode = True
