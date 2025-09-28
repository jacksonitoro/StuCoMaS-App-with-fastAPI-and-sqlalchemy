# sprint2/main.py
from sprint2.database import SessionLocal, Base, engine
from sprint2.models import Student, Instructor, Course, Enrollment
import sprint2.crud as crud

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Open a DB session
db = SessionLocal()

# --- 1. Create an Instructor ---
inst = crud.create_instructor(
    db,
    first_name="John",
    last_name="Doe",
    email="jdoe@uni.edu",
    department="Computer Science"
)

# --- 2. Create a Course assigned to Instructor ---
course = crud.create_course(
    db,
    code="CS101",
    title="Intro to Programming",
    credit_hours=3,   # ✅ matches crud.py now
    instructor_id=inst.id
)

# --- 3. Create Students ---
s1 = crud.create_student(db, "Alice", "Johnson", "alice@uni.edu")
s2 = crud.create_student(db, "Bob", "Smith", "bob@uni.edu")

# --- 4. Enroll Students in Course ---
crud.enroll_student(db, s1.id, course.id)
crud.enroll_student(db, s2.id, course.id)

# --- 5. Assign Grades ---
crud.assign_grade(db, s1.id, course.id, "A")
crud.assign_grade(db, s2.id, course.id, "B+")

# --- 6. Query Results ---
print("\n--- Students in Database ---")
for student in crud.get_students(db):
    print(f"{student.first_name} {student.last_name} ({student.email})")

print("\n--- Course Info ---")
print(f"{course.code} - {course.title}, Instructor: {inst.first_name} {inst.last_name}")

print("\n--- Enrollments ---")
enrollments = db.query(Enrollment).all()
for e in enrollments:
    student = db.query(Student).filter(Student.id == e.student_id).first()
    print(f"{student.first_name} {student.last_name} -> {course.code}, Grade: {e.grade}")

# Close session
db.close()
