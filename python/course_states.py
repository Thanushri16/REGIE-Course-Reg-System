# This file has the implementation of the state design pattern that uses 2 states to determine if a course is open or closed. 
# A course state is defined as open if the course enrollment count has not reached its maximum capacity. In this case, students can register for 
# the class. If a course state is closed, the course already reached its maximum enrollment and the students can't register for this course. 
from abc import ABCMeta, abstractmethod
from register_class import *

MAX_ENROLLMENT = 30  # Entered 5 due to testing purposes. In real world scenarios it would be around 40. 

class CourseContext(metaclass = ABCMeta):
    @abstractmethod
    def add_student(self, course_section, student):
        pass

class CourseOpen(CourseContext):
    def __init__(self, con):
        self.__con = con

    def add_student(self, course_section, student):
        # Import course section folder 
        # Implement Register class of student with scheduling aspects
        # Set_state implementation
        rc = RegisterClass(self.__con, student, course_section)
        rc.add_course_to_student()
        course_section.set_current_enrollment(course_section.get_current_enrollment() + 1)
        if course_section.get_current_enrollment() >= MAX_ENROLLMENT:
            self.set_state(course_section, student, self.__con)
        return 
    
class CourseClosed(CourseContext):
    def __init__(self, con):
        self.__con = con

    def add_student(self, course_section, student):
        if course_section.get_current_enrollment() < MAX_ENROLLMENT:
            self.set_state(course_section, student, self.__con)
        else:
            print("Student cannot be added to the course!")
        return 
    
class CourseAdd:
    # This is the class that initializes the course context and lets the course states to change
    def __init__(self, course_section, student, con) -> None:
        self.set_state(course_section, student, con)

    def set_state(self, course_section, student, con): 
        if course_section.get_current_enrollment() < MAX_ENROLLMENT:
            self.__current_state = CourseOpen(con)
        else: 
            self.__current_state = CourseClosed(con)
    
    def get_state(self):
        return self.__current_state

        
    
