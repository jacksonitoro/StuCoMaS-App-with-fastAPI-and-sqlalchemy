from StuCoMaS.sprint1.person import Person

class Student(Person):
    def __init__(self, student_id: int, first_name: str, last_name: str, email:str):
        super().__init__(student_id,first_name, last_name, email)
        self._enrollments = {}

    def enroll(self, course_code: str):
        if course_code not in self._enrollments:
            self._enrollments[course_code] = None
        else:
            print(f"Already enrolled in {course_code}")

    def set_grade(self, course_code: str, grade: int):
        if course_code not in self._enrollments:
            self._enrollments[course_code] = grade
        else:
            print(f"Not enrolled in {course_code}")

    def get_courses(self):
        return self._enrollments

    def __str__(self):
        return f"{self.get_name()} | Email: {self.get_email()} | Courses: {list(self._enrollments.keys())}"


