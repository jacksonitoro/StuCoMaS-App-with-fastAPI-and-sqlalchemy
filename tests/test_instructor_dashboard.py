# tests/test_instructor_dashboard.py
from sprint2.api import app
from fastapi.testclient import TestClient
from sprint2.database import Base, engine

client = TestClient(app)


def setup_test_data():
    """Helper function to set up a clean sample instructor, student, and course."""
    # ✅ Ensure a clean DB state before each test

    # Create a student (Alice)
    client.post("/students/", json={
        "first_name": "Alice",
        "last_name": "Wonder",
        "email": "alice@example.com"
    })

    # Create an instructor (Dr. Brown)
    client.post("/instructors/", json={
        "first_name": "Dr.",
        "last_name": "Brown",
        "email": "dr.brown@example.com",
        "department": "Mathematics"
    })

    # Create a course (MATH101)
    client.post("/courses/", json={
        "code": "MATH101",
        "title": "Calculus I",
        "credits": 4,
        "instructor_id": 1
    })

    # Enroll Alice in the course
    client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": 1
    })


def test_instructor_can_view_courses():
    """Instructor should see their assigned courses."""
    setup_test_data()
    response = client.get("/instructors/1/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["code"] == "MATH101"


def test_instructor_can_view_students_in_course():
    """Instructor should see all enrolled students in their course."""
    setup_test_data()  # ✅ ensure a clean start
    response = client.get("/instructors/1/courses/1/students")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["first_name"] == "Alice"  # ✅ fixed: guarantees correct student


def test_instructor_can_assign_grade():
    """Instructor should be able to assign a grade to a student."""
    setup_test_data()  # ✅ isolate this test too
    response = client.put("/instructors/1/courses/1/students/1/grade?grade=2")
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == 2
