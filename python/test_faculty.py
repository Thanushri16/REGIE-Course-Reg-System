import unittest
import pytest

from abstract_factory import *

class Test_Faculty: 
    '''
    Tests both valid and invalid cases of the "Faculty" class methods
    '''
    @pytest.mark.parametrize("id, expected", [(10023456, "Alex James"),(10034343, "Mark Shacklette"),\
        (78684440, None), (10034567, "Gerry Brady")])
    def test_retrieve_details(self, id, expected):
        # Checking if the retrieve function returns the details of faculty based on the input id
        faculty = Faculty()
        faculty.create_connection()
        assert faculty.retrieve_details(id) == expected

    @pytest.mark.parametrize("input, value, expected", [("name", "Geraldine Brady", {"name":"Geraldine Brady"}), \
         ("address", "Hyde Park,IL", {"address":"Hyde Park,IL"}),
         ("mobile", 2375237557, {"mobile":2375237557}), \
         ("email", "gerrybrady@cs.uchicago.edu", {"email":"gerrybrady@cs.uchicago.edu"}), \
            ("rank", "Clinical Professor", {"position":"Clinical Professor"}), \
                ("dept", 10056, {"dept_id": 10056}), \
                    ("status", "Part-Time", {"status":"Part-Time"})])
    def test_modify_profile(self, input, value, expected):
        faculty = Faculty()
        faculty.create_connection()
        faculty.retrieve_details(10034567)
        if input == "name":
            assert faculty.modify_profile(10034567, name = value) == expected
        if input == "address": 
            assert faculty.modify_profile(10034567, address = value) == expected
        if input == "mobile": 
            assert faculty.modify_profile(10034567, mobile = value) == expected
        if input == "email": 
            assert faculty.modify_profile(10034567, email = value) == expected
        if input == "rank":
            assert faculty.modify_profile(10034567, rank = value) == expected
        if input == "dept":
            assert faculty.modify_profile(10034567, dept = value) == expected
        if input == "status":
            assert faculty.modify_profile(10034567, status = value) == expected
        # cleanup - deleting the faculty after success of the test
        cursor = faculty.con.con.cursor()
        cursor.execute("delete from faculty where id = %s", (10034567,))
        faculty.con.con.commit()
        cursor.close()

    def test_initialize_details(self):
        # Checking if the initialize details function in faculty works correctly
        faculty = FacultyFactory().create_user(10034567, 'Gerry Brady', 'Chicago, IL', 1489924012, 'gerrybrady@uchicago.edu', 'passwordbrady', 'Associate Professor', 10053, 'Full-Time')
        faculty.create_connection()
        cursor = faculty.con.con.cursor()
        value = 10034567
        cursor.execute("select * from faculty where id = %s", (value,))
        assert (cursor.fetchone() == None) == True
        # executing the initialize details function
        faculty.initialize_details()
        # Executing the same select query again should not be empty
        cursor.execute("select * from faculty where id = %s", (value,))
        assert (cursor.fetchone()[0] == value) == True
        # cleanup - deleting the faculty after success of the test
        cursor.execute("delete from faculty where id = %s", (value,))
        faculty.con.con.commit()
        cursor.close()

    def test_view_department_information(self):
        # Checking if the retrieve function returns the details of faculty based on the input id
        faculty = FacultyFactory().create_user(10034567, 'Gerry Brady', 'Chicago, IL', 1489924012, 'gerrybrady@uchicago.edu', 'passwordbrady', 'Associate Professor', 10053, 'Full-Time')
        faculty.create_connection()
        faculty.initialize_details()
        assert faculty.view_department_information() == 'Department of Computer Science'

    def test_view_current_past_course_schedule(self): 
        faculty = Faculty()
        faculty.create_connection()
        faculty.retrieve_details(10023456)
        assert faculty.view_current_past_course_schedule() == [('Winter 2023', 900153251)]


#     def test_add_modify_student_scores(self) -> None:
#         assert Faculty(10023456, 'Alex', 'Austin, TX', 9144567990, 'alex@gmail.com', 'passwordalex',\
#             'Professor','Department of Computer Science','Part-Time').add_modify_student_scores('Fall 2022', 'MPCS50002-2', \
#                 12000001, "A1", 99) == False

#     def test_add_modify_student_grades(self) -> None:
#         assert Faculty(10023456, 'Alex', 'Austin, TX', 9144567990, 'alex@gmail.com', 'passwordalex',\
#             'Professor','Department of Computer Science','Part-Time').add_modify_student_grades('Fall 2022', 'MPCS50002-2', \
#                 12000001, "A") == False

#     def test_view_course_section_gradesheet(self) -> None:
#         assert Faculty(10023456, 'Alex', 'Austin, TX', 9144567990, 'alex@gmail.com', 'passwordalex',\
#             'Professor','Department of Computer Science','Part-Time').view_course_section_gradesheet('Fall 2022', 'MPCS50002-2') == True