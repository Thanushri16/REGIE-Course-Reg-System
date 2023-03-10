import unittest
import pytest

from student_course_section import *
from database_connect import *

class Test_StudentCourseSection:
    '''
    Tests both valid and invalid cases of the "Grade" class methods
    '''
    @pytest.fixture(scope="module")
    def db_connect(self):
        con = Connection.get_instance()
        con.connect()
        yield con
        con.close()

    def test_init_pass(self) -> None:
        # Checking if assert passes when valid values are passed to init function
        sc_section = StudentCourseSection(900153252, 'Winter 2023', 11000001)
        assert (sc_section.get_course_section_id() == 900153252 and sc_section.get_student_id() == 11000001\
                and sc_section.get_scores() == []) == True
        
    def test_init_fail(self) -> None:
        # Checking if assert fails when invalid values are passed to init function
        sc_section = StudentCourseSection(900153252, 'Winter 2023', 11000001)
        assert (sc_section.get_course_section_id() == 900153252 and sc_section.get_student_id() == 11000000\
                and sc_section.get_scores() == []) ==  False

    
    @pytest.mark.parametrize("quarter, course_section_id, student, task, score, expected", \
        [('Winter 2023', '900153251', [11000003, 11000004], 0, 96, True), ('Winter 2022', '900153251', [11000003, 11000004], 0, 96, False)])
    def test_assign_or_modify_scores(self, db_connect, quarter, course_section_id, student, task, score, expected) -> None:
        # Checking if assign_or_modify_scores() works
        assert StudentCourseSection().assign_or_modify_scores(db_connect, quarter, course_section_id, student, task, score) == expected

    @pytest.mark.parametrize("quarter, course_section_id, student, grade, expected", \
        [('Winter 2023', '900153251', [11000004], 'A', True)])
    def test_assign_or_modify_grades(self, db_connect, quarter, course_section_id, student, grade, expected) -> None:
        # Checking if assign_or_modify_grades() works
        assert StudentCourseSection().assign_or_modify_grades(db_connect, quarter, course_section_id, student, grade) == expected

    @pytest.mark.parametrize("quarter, course_section_id, student, expected", \
        [('Winter 2023', '900153251', [11000004], True), ('Winter 2023', '900153251', [], True)])
    def test_view_coursesection_gradesheet(self, db_connect, quarter, course_section_id, student, expected) -> None:
        # Checking if view_coursesection_gradesheet() works
        assert StudentCourseSection().view_coursesection_gradesheet(db_connect, quarter, course_section_id, student) == expected

    @pytest.mark.parametrize("student_id, expected", \
        [(11000000, True), (11000007, False)])
    def test_calculate_avg_gpa(self, db_connect, student_id, expected) -> None:
        # Checking if calculate_avg_gpa() works
        assert StudentCourseSection().calculate_avg_gpa(db_connect, student_id) == expected