# main.py
from student import Student
from StuCoMaS.sprint1.instructor import Instructor
from StuCoMaS.sprint1.course import Course

# Create instructor
inst = Instructor(1, "John", "Doe", "jdoe@uni.edu", "Computer Science")

# Create course
course = Course("CS101", "Intro to Programming", 3)
course.assign_instructor(inst)

# Create students
s1 = Student(101, "Alice", "Johnson", "alice@uni.edu")
s2 = Student(102, "Bob", "Smith", "bob@uni.edu")

# Enroll students
course.enroll_student(s1)
course.enroll_student(s2)

# Assign grades
s1.set_grade("CS101", "A")
s2.set_grade("CS101", "B+")

# Display results
print(course)
print(inst)
print(s1)
print(s2)
print("Students in course:", course.get_students())
