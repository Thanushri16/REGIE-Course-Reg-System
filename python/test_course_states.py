# Testing if the course_states sets the course states accurately.
import unittest
import pytest

from course_states import *
from database_connect import *

class Test_CourseAdd:
    '''
    Tests both valid and invalid cases of the "CourseStates" class methods
    '''
    @pytest.fixture(scope="module")
    def db_connect(self):
        con = Connection.get_instance()
        con.connect()
        yield con
        con.close()

    def test_course_add(self, db_connect):
        # Adding a new course section 
        course_section1 = CourseSection()
        course_section1.retrieve_course_section(db_connect, 'Winter 2023', 900153251)
        course_adder1 = CourseAdd(course_section1, 11000007, db_connect)
        assert course_adder1.get_state().add_student(course_section1, 11000007) == None
        CourseSection(900153252, 'Winter 2023', 90015325, 207, "Friday", "16:30:00", "17:30:00", False).add_course_section(db_connect) 
        course_section2 = CourseSection()
        course_section2.retrieve_course_section(db_connect, 'Winter 2023', 900153252)
        course_adder2 = CourseAdd(course_section2, 11000007, db_connect)
        assert course_adder2.get_state().add_student(course_section2, 11000007) == None
        CourseSection().delete_course_section(db_connect, 'Winter 2023', 900153252)
    