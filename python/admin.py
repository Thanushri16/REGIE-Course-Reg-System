from user import *
from course_section import *
from database_connect import *

# Concrete Admin Class
class Admin(User):
    def __init__(self, id='', name='', address='', mobile='', email='', password='') -> None:
        self.con = None
        super().__init__(id, name, address, mobile, email, password)

    def get_type(self):
        return "Admin"

    def create_connection(self):
        self.con = Connection.get_instance()
        self.con.connect()

    def close_connection(self):
        if self.con: 
            self.con.close()
            print("Connection to MySQL database closed!")
        else:
            print("No database connection exists!")

    def initialize_details(self):
        # This function persists the admin details in the database
        query = "insert into Admin (id, name, address, mobile, email, password) values (%s,%s,%s,%s,%s,%s)"
        values = (self._id, self._name, self._address, self._mobile, self._email, self._password)
        cursor = self.con.con.cursor()
        cursor.execute(query, values)
        self.con.con.commit()
        cursor.close()

    def retrieve_details(self, id):
        # This function takes as input an id from the admin and retrives the admin details
        query = "select * from admin where id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        cursor.close()
        if results:
            super().__init__(results[0], results[1], results[2], results[3], results[4], results[5])
            return self._name
        else:
            return None

    def modify_profile(self, name='', address='', mobile='', email='', password='', repassword=''):
        d = super().modify_profile(name, address, mobile, email, password, repassword)
        cursor = self.con.con.cursor()
        for key, value in d.items():
            query = "update Admin set " + key + " = %s where id = %s"
            values = (value, self._id)
            cursor.execute(query, values)
            self.con.con.commit()
        cursor.close()
        return d

    def add_student(self, id, name, address, mobile, email, password, restrictions, advisor, gpa, is_full_time, dept_id = '', expected_graduation = '', concentration = '') -> bool:
        # Function that adds a student to the student database
        # check if a student with the same id is already there in the database
        cursor = self.con.con.cursor()
        if is_full_time:
            query = "insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, name, address, mobile, email, password, restrictions, advisor, gpa, True, dept_id, expected_graduation, concentration)
            
        else:
            query = "insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, name, address, mobile, email, password, restrictions, advisor, gpa, False, None, None, None)
        
        cursor.execute(query, values)
        self.con.con.commit()
        cursor.close()
        print("Student added!")
        return True

    def delete_student(self, id) -> bool:
        # Function that deletes a student from the student database
        # return false if the student id is not there in the database
        cursor = self.con.con.cursor()
        query = "delete from student where id = %s"
        cursor.execute(query, (id,))
        self.con.con.commit()
        cursor.close()
        print("Student deleted!")
        return True
    
    def add_instructor(self, id, name, address, mobile, email, password, rank, dept, status) -> bool:
        # Function that adds an instructor to the faculty database
        # Check if the instructor id is already in the instructor database
        cursor = self.con.con.cursor()
        query = "insert into faculty values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (id, name, address, mobile, email, password, rank, dept, status)
        cursor.execute(query, values)
        self.con.con.commit()
        cursor.close()
        print("Faculty added!")
        return True

    def delete_instructor(self, id) -> bool:
        # Function that deletes an instructor from the instructor database
        # return false if the faculty id is not there in the database
        cursor = self.con.con.cursor()
        query = "delete from faculty where id = %s"
        cursor.execute(query, (id,))
        self.con.con.commit()
        cursor.close()
        print("Faculty deleted!")
        return True

    def add_course(self, id = '', name = '', description = '', dept_id = '', fee = '') -> bool:
        # Function that lets the admin to create a course in the course database
        return Course(id, name, description, dept_id, fee).add_course(self.con)
    
    def delete_course(self, id = '') -> bool:
        # Function that lets the admin to delete a course in the course database
        return Course().delete_course(self.con, id)

    def modify_course(self, id, name='', description='', dept_id='', fee='') -> bool:
        # Function that lets the admin to modify a course in the course database
        return Course().modify_course_details(self.con, id, name, description, dept_id, fee)

    def drop_course_sections_lessthan5(self, quarter) -> bool:
        # Drops the course section if course section has less than 5 students
        return CourseSection().delete_course_sections_lessthan5(self.con, quarter)
    
    def add_course_section(self, course_section_id='', quarter_id='', course_id='', room_id='', day='', start_time='', end_time='', permission_required=''):
        return CourseSection(course_section_id, quarter_id, course_id, room_id, day, start_time, end_time, permission_required).add_course_section(self.con)
    
    def delete_course_section(self, course_section_id = '', quarter = ''):
        return CourseSection().delete_course_section(self.con, quarter, course_section_id)
    
    def add_instructor_coursesection(self, course_section_id, quarter, faculty):
        return CourseSection().add_instructor(self.con, quarter, course_section_id, faculty)
    
    def delete_instructor_coursesection(self, course_section_id, quarter, faculty):
        return CourseSection().delete_instructor(self.con, quarter, course_section_id, faculty)