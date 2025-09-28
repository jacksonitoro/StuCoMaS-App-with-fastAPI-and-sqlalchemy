
class Course:
    def __init__(self, code: str, title: str, credits: int, instructor=None):
        self._code = code
        self._title = title
        self._credits = credits
        self._instructor = instructor
        self._students = []

    def assign_instructor(self, instructor):
        self._instructor = instructor
        instructor.assign_course(self._code)

    def enroll_student(self, student):
        if student not in self._students:
            self._students.append(student)
            student.enroll(self._code)

    def get_students(self):
        return [s.get_name() for s in self._students]

    def __str__(self):
        instructor_name = self._instructor.get_name() if self._instructor else "TBA"
        return (f"Course: {self._code} - {self._title} "
                f"({self._credits} credits) | Instructor: {instructor_name}")
