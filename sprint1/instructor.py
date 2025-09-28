
from person import Person

class Instructor(Person):
    def __init__(self, instructor_id: int, first_name: str, last_name: str, email: str, department: str):
        super().__init__(instructor_id, first_name, last_name, email)
        self._department = department
        self._courses = []  # list of course codes

    def assign_course(self, course_code: str):
        if course_code not in self._courses:
            self._courses.append(course_code)

    def get_courses(self):
        return self._courses

    def __str__(self):
        return f"Instructor: {self.get_name()} ({self._department}) | Courses: {self._courses}"
