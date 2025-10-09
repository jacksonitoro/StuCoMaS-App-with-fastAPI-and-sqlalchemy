from pydantic import BaseModel, EmailStr, conint, ConfigDict
from typing import Optional, List


# ============================================================
# 🎓 STUDENTS
# ============================================================

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 👩‍🏫 INSTRUCTORS
# ============================================================

class InstructorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: Optional[str] = None


class InstructorCreate(InstructorBase):
    pass


class Instructor(InstructorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 📘 COURSES
# ============================================================

class CourseBase(BaseModel):
    code: str
    title: str
    credits: int


class CourseCreate(CourseBase):
    instructor_id: int


class Course(CourseBase):
    id: int
    instructor: Optional[Instructor] = None
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 🧾 ENROLLMENTS
# ============================================================

class EnrollmentBase(BaseModel):
    grade: Optional[conint(ge=1, le=5)] = None


class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int


class Enrollment(EnrollmentBase):
    student: Optional[Student] = None
    course: Optional[Course] = None
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 🔢 GRADE UPDATE
# ============================================================

class EnrollmentGradeUpdate(BaseModel):
    grade: conint(ge=1, le=5)


# ============================================================
# 📊 DASHBOARD RESPONSES
# ============================================================

class StudentWithGrades(Student):
    grades: List[Enrollment] = []


class CourseWithStudents(Course):
    students: List[Student] = []


# ============================================================
# 🧠 NEW: STUDENT GRADE SCHEMA
# ============================================================

class StudentGrade(BaseModel):
    course: str
    grade: Optional[int]

    model_config = ConfigDict(from_attributes=True)
