import unittest
import pytest

from abstract_factory import *
from user import *
from admin import *
from faculty import *
from student import *
from part_time_student import *
from full_time_student import *

class Test_Admin:
    '''
    Tests both valid and invalid cases of the "Admin" class methods
    '''
    def test_init_pass(self) -> None:
        # Checking if assert passes when valid values are passed to init function
        admin = AdminFactory().create_user(12334889, 'Thanushri', 'Chicago, IL', 1234567890, 'thanushritharun@gmail.com', 'password1')
        assert (admin.get_name() == 'Thanushri' and admin.get_address() == 'Chicago, IL' and admin.get_mobile() == 1234567890 \
            and admin.get_email() == 'thanushritharun@gmail.com') == True

    def test_init_fail(self) -> None:
        # Checking if assert fails when invalid values are passed to init function
        admin = AdminFactory().create_user(12334889, 'Thanushri', 'Chicago, IL', 1234567890, 'thanushri@gmail.com', 'password1')
        assert (admin.get_name() == 'Thanushri' and admin.get_address() == 'Chicago, IL' and admin.get_mobile() == 1234567890 \
            and admin.get_email() == 'thanushritharun@gmail.com') == False


class Test_Student: 
    '''
    Tests both valid and invalid cases of the "Student" class methods
    '''

    def test_init_pass(self) -> None:
        # Checking if assert passes when valid values are passed to init function
        student = FullTimeStudentFactory().create_student(11000000, 'Zoya', 'Boston, MA', 1234567990, 'zoya@gmail.com', 'passwordzoya',\
            {'medical': True, 'course_load': False}, 'Ram Advisor', 3.7, 10053,"2023-03-11", 'Software Engineering')
        assert (student.get_name() == 'Zoya' and student.get_address() == 'Boston, MA' and student.get_mobile() == 1234567990 \
            and student.get_email() == 'zoya@gmail.com' and student.get_restrictions() == {'medical': True, 'course_load': False} and \
                student.get_advisor() == 'Ram Advisor' and student.get_gpa() == 3.7 and student.get_student_status() == "Full-Time student") == True

    def test_init_fail(self) -> None:
        # Checking if assert fails when invalid values are passed to init function
        student = FullTimeStudentFactory().create_student(11000000, 'Zoya', 'Boston, MA', 1234567990, 'zoya@gmail.com', 'passwordzoya',\
            {'medical': True, 'course_load': False}, 'Ram Advisor', 3.7,10053,"2023-03-11", 'Software Engineering')
        assert (student.get_name() == 'Zoya' and student.get_address() == 'Boston, MA' and student.get_mobile() == 1234567990 \
            and student.get_email() == 'zoya@gmail.com' and student.get_restrictions() == {'medical': True, 'course_load': False} and \
                student.get_advisor() == 'Ram Advisor' and student.get_gpa() == 3.7 and student.get_student_status() == "Part-Time student") == False


class Test_Faculty: 
    '''
    Tests both valid and invalid cases of the "Faculty" class methods
    '''

    def test_init_pass(self) -> None:
        # Checking if assert passes when valid values are passed to init function
        faculty = FacultyFactory().create_user(10023456, 'Alex', 'Austin, TX', 9144567990, 'alex@gmail.com', 'passwordalex',\
            'Professor','Department of Computer Science','Full-Time')
        assert (faculty.get_name() == 'Alex' and faculty.get_address() == 'Austin, TX' and faculty.get_mobile() == 9144567990 \
            and faculty.get_email() == 'alex@gmail.com' and faculty.get_rank() == 'Professor'\
            and faculty.get_dept() == 'Department of Computer Science' and faculty.get_fulltimestatus() == 'Full-Time') == True

    def test_init_fail(self) -> None:
        # Checking if assert fails when invalid values are passed to init function
        faculty = FacultyFactory().create_user(10023456, 'Alex', 'Austin, TX', 9144567990, 'alex@gmail.com', 'passwordalex',\
            'Professor','Department of Computer Science','Full-Time')
        assert (faculty.get_name() == 'Alex' and faculty.get_address() == 'Austin, TX' and faculty.get_mobile() == 9144567990 \
            and faculty.get_email() == 'alex@gmail.com' and faculty.get_rank() == 'Assistant Professor'\
            and faculty.get_dept() == 'Department of Computer Science' and faculty.get_fulltimestatus() == 'Full-Time') == False
            