# Abstract Factory pattern is used in python that creates different types of users including Faculty, Admin and Student
# using the factory pattern with inheritance for Part-Time Student and Full-Time Student from the Student class:

from abc import ABC, abstractmethod
from user import *
from admin import Admin
from faculty import *
from student import *
from part_time_student import *
from full_time_student import *

# Abstract Factory for User
class UserFactory(ABC):
    @abstractmethod
    def create_user(self, id, name, address, mobile, email, password) -> None:
        pass

# Concrete Factory for Faculty
class FacultyFactory(UserFactory):
    def create_user(self, id, name, address, mobile, email, password, rank, dept, status) -> None:
        return Faculty(id, name, address, mobile, email, password, rank, dept, status)

# Concrete Factory for Admin
class AdminFactory(UserFactory):
    def create_user(self, id, name, address, mobile, email, password) -> None:
        return Admin(id, name, address, mobile, email, password)

# Abstract Factory for Student
class StudentFactory(ABC):
    @abstractmethod
    def create_student(self, id, name, address, mobile, email, password, restrictions, advisor, gpa) -> None:
        pass

# Concrete Factory for Part Time Student
class PartTimeStudentFactory(StudentFactory):
    def create_student(self, id, name, address, mobile, email, password, restrictions, advisor, gpa) -> None:
        return PartTimeStudent(id, name, address, mobile, email, password, restrictions, advisor, gpa)

# Concrete Factory for Full Time Student
class FullTimeStudentFactory(StudentFactory):
    def create_student(self, id, name, address, mobile, email, password, restrictions, advisor, gpa, dept_id, expected_graduation, concentration) -> None:
        return FullTimeStudent(id, name, address, mobile, email, password, restrictions, advisor, gpa, dept_id, expected_graduation, concentration)

# Creating a Full-Time student object with FullTimeStudentFactory
# full_time_factory = FullTimeStudentFactory()
# full_time_student = full_time_factory.create_student(11000000, 'Zoya', 'Boston, MA', 1234567990, 'zoya@gmail.com', 'passwordzoya',\
#             {'medical': True, 'course_load': False}, 'Ram Advisor', 3.6)
# print(full_time_student.get_name())  
# print(full_time_student.get_email())  
# print(full_time_student.get_gpa())
# print(full_time_student.get_student_status()) 