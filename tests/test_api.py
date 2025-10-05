def test_create_student(client):
    response = client.post("/students/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "John"
    assert data["email"] == "john.doe@example.com"


def test_get_students(client):
    response = client.get("/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_instructor(client):
    response = client.post("/instructors/", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "department": "Computer Science"
    })
    assert response.status_code == 200


def test_create_course(client):
    response = client.post("/courses/", json={
        "code": "CS101",
        "title": "Intro to CS",
        "credits": 3,
        "instructor_id": 1
    })
    assert response.status_code == 200, response.text


def test_enroll_student(client):
    response = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": 1
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert "student" in data and "course" in data


def test_assign_grade(client):
    response = client.put("/enrollments/1/1/grade", json={"grade": 2})
    assert response.status_code == 200, response.text
    assert response.json()["grade"] == 2


def test_search_students(client):
    response = client.get("/students/search?query=john")
    assert response.status_code == 200


def test_search_courses(client):
    response = client.get("/courses/search?query=CS101")
    assert response.status_code == 200
