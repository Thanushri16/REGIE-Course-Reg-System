import unittest
import pytest

from course import *
from database_connect import *

class Test_Course:
    '''
    Tests both valid and invalid cases of the "Course" class methods
    '''
    @pytest.fixture(scope="module")
    def db_connect(self):
        con = Connection.get_instance()
        con.connect()
        yield con
        con.close()

    def test_init_pass(self, db_connect) -> None:
        # Checking if assert passes when valid values are passed to init function
        course = Course(90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500)
        assert (course.get_course_id() == 90015327 and course.get_course_name() == 'Advanced Algorithms'\
            and course.get_dept_info(db_connect) == 'Department of Computer Science') == True

    def test_init_fail(self, db_connect) -> None:
        # Checking if assert fails when invalid values are passed to init function
        course = Course(90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500)
        assert (course.get_course_id() == 90015326 and course.get_course_name() == 'Advanced Algorithms'\
            and course.get_dept_info(db_connect) == 'Department of Computer Science') == False

    @pytest.mark.parametrize("id, expected", [(90015327, (90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500)),\
        (90015390, None)])
    def test_retrieve_course(self, db_connect, id, expected) -> None:
        assert Course().retrieve_course(db_connect, id) == expected

    @pytest.mark.parametrize("course_id, expected", [(90015390, False), (90015327, True)])
    def test_delete_course(self, db_connect, course_id, expected) -> None:
        # Checking if delete_course() works
        assert Course().delete_course(db_connect, course_id) == expected

    @pytest.mark.parametrize("course_id, name, description, dept, fee, expected",\
        [(90015326, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500, False), \
        (90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500, True)])
    def test_add_course(self, db_connect, course_id, name, description, dept, fee, expected) -> None:
        # Checking if add_course() works
        course = Course(course_id, name, description, dept, fee)
        assert course.add_course(db_connect) == expected

    @pytest.mark.parametrize("course_id, variable, test_input, expected", [(90015327,'name','Advanced Algorithms', False), \
        (90015327,'name','Functional Programming', True), (90015390,'name','', False), (90015327,'description','Advanced Programming concepts', False), 
        (90015327,'description','Advanced Func. Programming', True), (90015390,'description','', False), \
        (90015327,'dept', 10053, False), (90015327,'dept', 10056, True), (90015327,'dept', None, False), \
        (90015390,'dept', 10053, False), (90015327,'fee',6500, False), (90015327,'fee',7500, True), (90015390,'fee','',False)])
    def test_modify_course_details(self, db_connect, course_id, variable, test_input, expected) -> None:
        # Checking if modify_course_details() works
        course = Course()
        if variable == 'name':
            assert course.modify_course_details(db_connect, course_id, name=test_input) == expected
        elif variable == 'description':
            assert course.modify_course_details(db_connect, course_id, description=test_input) == expected
        elif variable == 'dept':
            assert course.modify_course_details(db_connect, course_id, dept_id=test_input) == expected
        elif variable == 'fee': 
            assert course.modify_course_details(db_connect, course_id, fee=test_input) == expected
