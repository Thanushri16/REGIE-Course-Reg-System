import unittest
import pytest

from abstract_factory import *

class Test_Admin:
    '''
    Tests both valid and invalid cases of the "Admin" class methods
    '''
    @pytest.mark.parametrize("id, expected", [(78684436, "Karin Czaplewski"),(78684435, "Molly Stoner"),\
        (78684440, None)])
    def test_retrieve_details(self, id, expected):
        # Checking if the retrieve function returns the details of admin based on the input id
        admin = Admin()
        admin.create_connection()
        assert admin.retrieve_details(id) == expected

    @pytest.mark.parametrize("input, value, expected", [("name", "Borja Sortamayor", {"name":"Borja Sortamayor"}), \
         ("address", "Hyde Park,IL", {"address":"Hyde Park,IL"}),
         ("mobile", 8604728572, {"mobile":8604728572}), \
         ("email", "borja@cs.uchicago.edu", {"email":"borja@cs.uchicago.edu"})])
    def test_modify_profile(self, input, value, expected):
        admin = Admin()
        admin.create_connection()
        admin.retrieve_details(78684439)
        if input == "name":
            assert admin.modify_profile(name = value) == expected
        if input == "address": 
            assert admin.modify_profile(address = value) == expected
        if input == "mobile": 
            assert admin.modify_profile(mobile = value) == expected
        if input == "email": 
            assert admin.modify_profile(email = value) == expected
        # cleanup - deleting the admin after success of the test
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()


    def test_initialize_details(self):
        # Checking if the initialize details function in admin works correctly
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        cursor = admin.con.con.cursor()
        value = 78684439
        cursor.execute("select * from admin where id = %s", (value,))
        assert (cursor.fetchone() == None) == True
        # executing the initialize details function
        admin.initialize_details()
        # Executing the same select query again should not be empty
        cursor.execute("select * from admin where id = %s", (value,))
        assert (cursor.fetchone()[0] == value) == True
        # cleanup - deleting the admin after success of the test
        cursor.execute("delete from admin where id = %s", (value,))
        admin.con.con.commit()
        cursor.close()

    @pytest.mark.parametrize("id, name, address, mobile, email, password, restrictions, advisor, gpa, is_full_time, expected",\
        [(11000005, 'Swetha', 'Boston, MA', 1234567830, 'swetha@uchicago.edu', 'passwordswetha',\
            "medical", 'Andrew Wang', 3.4, False, True)])
    def test_add_student(self, id, name, address, mobile, email, password, restrictions, advisor, gpa, is_full_time, expected) -> None:
        # Checking if add_student() works
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        admin.initialize_details()
        assert admin.add_student(id, name, address, mobile, email, password, restrictions, advisor, gpa, is_full_time) == expected
        # cleanup - deleting the admin after success of the test
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()


    @pytest.mark.parametrize("id, expected",[(11000005, True)])
    def test_delete_student(self, id, expected) -> None:
        # Checking if delete_student() works
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        admin.initialize_details()
        assert admin.delete_student(id) == expected
        # cleanup - deleting the admin after success of the test
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()

    def test_delete_course(self) -> None:
        # Checking if delete_course() works
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        admin.initialize_details()
        assert admin.delete_course(90015327) == True
        # cleanup 
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()

    def test_add_course(self) -> None:
        # Checking if add_course() works
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        admin.initialize_details()
        assert admin.add_course(90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500) == True
        # cleanup 
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()

    def test_modify_course(self) -> None:
        # Checking if modify_course() works
        admin = AdminFactory().create_user(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja')
        admin.create_connection()
        admin.initialize_details()
        assert admin.modify_course(90015327, 'Functional Programming') == True
        # cleanup - deleting the admin after success of the test
        admin.delete_course(90015327)
        admin.add_course(90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500) == True
        cursor = admin.con.con.cursor()
        cursor.execute("delete from admin where id = %s", (78684439,))
        admin.con.con.commit()
        cursor.close()