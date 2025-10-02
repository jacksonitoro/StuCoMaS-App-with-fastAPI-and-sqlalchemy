from pydantic import BaseModel, EmailStr, conint
from typing import Optional

# --- Students ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


# --- Instructors ---
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
        from_attributes = True


# --- Courses ---
class CourseBase(BaseModel):
    code: str
    title: str
    credits: int

class CourseCreate(CourseBase):
    instructor_id: int

class Course(CourseBase):
    id: int
    instructor: Instructor  # nested Instructor

    class Config:
        from_attributes = True


# --- Enrollments ---
class EnrollmentBase(BaseModel):
    grade: Optional[int] = None

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int

class Enrollment(EnrollmentBase):
    student: Student  # nested Student
    course: Course    # nested Course

    class Config:
        from_attributes = True


# --- Grade Update ---
class EnrollmentGradeUpdate(BaseModel):
    grade: conint(ge=1, le=5)  # enforce 1 ≤ grade ≤ 5