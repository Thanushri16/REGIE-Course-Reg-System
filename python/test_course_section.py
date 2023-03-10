import unittest
import pytest

from course_section import *
from database_connect import *

class Test_Course_Section:
    '''
    Tests both valid and invalid cases of the "CourseSection" class methods
    '''
    @pytest.fixture(scope="module")
    def db_connect(self):
        con = Connection.get_instance()
        con.connect()
        yield con
        con.close()

    def test_init_pass(self) -> None:
        # Checking if assert passes when valid values are passed to init function
        course_section = CourseSection(900153261, 'Spring 2023', 90015326, 205, "Wednesday", "17:30:00", "19:30:00", False)
        assert (course_section.get_course_id() == 90015326 and course_section.get_quarter_id() == "Spring 2023" and course_section.get_end_time() == "19:30:00") == True
        
    def test_init_fail(self) -> None:
        # Checking if assert fails when invalid values are passed to init function
        course_section = CourseSection(900153261, 'Spring 2023', 90015326, 205, "Wednesday", "17:30:00", "19:30:00", False)
        assert (course_section.get_course_id() == 900153261 and course_section.get_quarter_id() == "Spring 2023" and course_section.get_end_time() == "20:30:00") == False

    @pytest.mark.parametrize("quarter, id, expected", [('Winter 2023', 900153252, (900153252, 'Winter 2023', 90015325)),\
        ('Winter 2023', 900153253, None), ('Winter 2024', 900153252, None)])
    def test_retrieve_course_section(self, db_connect, quarter, id, expected):
        # Checking if retrieve_course_section works
        assert CourseSection().retrieve_course_section(db_connect, quarter, id) == expected

    @pytest.mark.parametrize("quarter, id, expected", [('Winter 2023', 900153251, 'Object Oriented Programming'),\
        ('Winter 2023', 9001532, None), ('Winter 2024', 900153251, None)])
    def test_get_name_of_coursesection(self, db_connect, quarter, id, expected):
        # Checking if retrieve_course_section works
        assert CourseSection().get_name_of_coursesection(db_connect, quarter, id) == expected

    @pytest.mark.parametrize("quarter, id, expected", [('Winter 2023', 900153251, [11000000,11000001,11000002,11000003,11000004]),\
        ('Winter 2023', 900153261, None), ('Winter 2024', 900153253, None)])
    def test_view_enrolled_students(self, db_connect, quarter, id, expected) -> None:
        # Checking if view_enrolled_students() works
        assert CourseSection().view_enrolled_students(db_connect, quarter, id) == expected

    @pytest.mark.parametrize("course_section_id, quarter_id, course_id, room_id, day, start_time, end_time, permission_required, expected",\
        [(900153261, 'Spring 2023', 90015326, 205, "Wednesday", "17:30:00", "19:30:00", False, True), \
        (900153251,'Winter 2023', 90015325, 205, 'Wednesday', '17:30:00','19:30:00', False, False)])
    def test_add_course_section(self, db_connect, course_section_id, quarter_id, course_id, room_id, day, start_time, end_time, permission_required, expected) -> None:
        # Checking if add_course_section() works
        assert CourseSection(course_section_id, quarter_id, course_id, room_id, day, start_time, end_time, permission_required).add_course_section(db_connect) == expected

    @pytest.mark.parametrize("quarter,course_section_id,expected",[('Spring 2023', 900153261, True),('Spring 2023', 900153261, False)])
    def test_delete_course_section(self, db_connect, quarter, course_section_id, expected) -> None:
        # Checking if delete_course_section() works
        assert CourseSection().delete_course_section(db_connect, quarter, course_section_id) == expected

    @pytest.mark.parametrize("quarter,expected",[('Winter 2023', True),('Spring 2023', False)])
    def test_delete_course_sections_lessthan5(self, db_connect, quarter, expected) -> None:
        # Checking if delete_course_sections_lessthan5() works
        assert CourseSection().delete_course_sections_lessthan5(db_connect, quarter) == expected

    @pytest.mark.parametrize("quarter,course_section_id,student,expected",[('Winter 2023', 900153251, [1100006, 11000007], True),('Spring 2023', 900153261, [11000000, 11000003], False)])
    def test_add_student(self, db_connect, quarter, course_section_id, student, expected) -> None:
        # Checking if add_student() works
        assert CourseSection().add_student(db_connect, quarter, course_section_id, student) == expected

    @pytest.mark.parametrize("quarter,course_section_id,student,expected",[('Winter 2023', 900153251, [1100006, 11000007], True),('Spring 2023', 900153261, [11000000, 11000003], False)])
    def test_delete_student(self, db_connect, quarter, course_section_id, student, expected) -> None:
        # Checking if delete_student() works
        assert CourseSection().delete_student(db_connect, quarter, course_section_id, student) == expected

    @pytest.mark.parametrize("quarter,course_section_id,faculty,expected",[('Winter 2023', 900153251, [12591910], True),('Spring 2023', 900153261, [12591910], False)])
    def test_add_instructor(self, db_connect, quarter, course_section_id, faculty, expected) -> None:
        # Checking if add_instructor() works
        assert CourseSection().add_instructor(db_connect, quarter, course_section_id, faculty) == expected

    @pytest.mark.parametrize("quarter,course_section_id,faculty,expected",[('Winter 2023', 900153251, [12591910], True),('Spring 2023', 900153261, [12591910], False)])
    def test_delete_instructor(self, db_connect, quarter, course_section_id, faculty, expected) -> None:
        # Checking if delete_instructor() works
        assert CourseSection().delete_instructor(db_connect, quarter, course_section_id, faculty) == expected