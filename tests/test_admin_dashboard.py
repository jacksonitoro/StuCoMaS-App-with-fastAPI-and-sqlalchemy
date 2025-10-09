# tests/test_admin_dashboard.py
from sprint2.api import app
from fastapi.testclient import TestClient
from sprint2.database import Base, engine

client = TestClient(app)


def setup_test_data():
    """Helper function to set up sample instructor, student, and course."""
    # ✅ Reset the database before inserting data


    # Create a student
    client.post("/students/", json={
        "first_name": "Bob",
        "last_name": "Marley",
        "email": "bob@example.com"
    })

    # Create an instructor
    client.post("/instructors/", json={
        "first_name": "Prof.",
        "last_name": "Adams",
        "email": "adams@example.com",
        "department": "Physics"
    })

    # ✅ Create a Physics course (matches test expectation)
    client.post("/courses/", json={
        "code": "PHY101",
        "title": "Classical Mechanics",
        "credits": 3,
        "instructor_id": 1
    })

    # Enroll student in course
    client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": 1
    })


def test_admin_can_view_all_enrollments():
    setup_test_data()
    response = client.get("/admin/enrollments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # ✅ Now matches the setup
    assert data[0]["course"]["code"] == "PHY101"


def test_admin_can_assign_grade_to_any_student():
    response = client.put("/admin/students/1/courses/1/grade?grade=3")
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == 3


def test_admin_can_reassign_grade():
    response = client.put("/admin/students/1/courses/1/grade?grade=1")
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == 1
