from user import *
from student_course_section import *
from database_connect import *
from department import *
from modify_features import *

# Concrete Faculty Class
class Faculty(User):
    def __init__(self, id='', name='', address='', mobile='', email='', password='', rank='', dept='', status='') -> None:
        super().__init__(id, name, address, mobile, email, password)
        self._rank = rank
        self._dept = dept
        self._status = status
        self.con = None

    def get_type(self):
        return "Faculty"

    def get_rank(self) -> str:
        return self._rank

    def get_dept(self) -> str:
        return self._dept

    def get_fulltimestatus(self):
        return self._status

    def set_rank(self, val) -> bool:
        if len(val) > 0:
            self._rank = val
            return True
        return False

    def set_dept(self, val) -> bool:
        self._dept = val
        return True

    def set_fulltimestatus(self, val) -> bool:
        self._status = val
        return True

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
        # This function persists the faculty details in the database
        query = "insert into faculty (id, name, address, mobile, email, password, position, dept_id, status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (self._id, self._name, self._address, self._mobile, self._email, self._password, self._rank, self._dept, self._status)
        cursor = self.con.con.cursor()
        cursor.execute(query, values)
        self.con.con.commit()
        cursor.close()

    def retrieve_details(self, id):
        # This function takes as input an id from the faculty and retrives the faculty details
        query = "select * from faculty where id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        if results:
            super().__init__(results[0], results[1], results[2], results[3], results[4], results[5])
            self._rank = results[6]
            self._dept = results[7]
            self._status = results[8]
            return self._name
        else:
            return None

    def modify_profile(self, id, name='', address='', mobile='', email='', password='', repassword='', rank='', dept='', status='') -> bool:
        flag = False
        d = {}
        if name or address or mobile or email or password or repassword:
            d = super().modify_profile(name, address, mobile, email, password, repassword)
            flag = True
        if rank:
            flag = self.set_rank(rank)
            d["position"] = rank
        if dept: 
            flag = self.set_dept(dept)
            d["dept_id"] = dept
        if status: 
            flag = self.set_fulltimestatus(status)
            d["status"] = status
        if flag:
            print("Changes made to faculty profile")
        return d

    def view_department_information(self): 
        # lets the faculty view the department information by passing dept id from their object to the Department Class
        # Interacts with Department
        query = "select * from department where id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (self._dept,))
        results = cursor.fetchone()
        if results:
            d = Department(results[0], results[1], results[3], results[2])
            return d.get_dept_name()
        else:
            return None

    def view_current_past_course_schedule(self): 
        # retrives the current or the past course schedule of the faculty
        query = "select * from FacultyCourseSection where faculty_id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (self._id, ))
        results = cursor.fetchall()
        if results: 
            course_sections = [(x[0], x[1]) for x in results]
            return course_sections
        else:
            return None

    def add_modify_student_scores(self, quarter = '', course_section_id = '', student = [], task = '', score = 0) -> bool:
        return StudentCourseSection().assign_or_modify_scores(self.con, quarter, course_section_id, student, task, score)

    def add_modify_student_grades(self, quarter = '', course_section_id = '', student = [], grade = '') -> bool:
        return StudentCourseSection().assign_or_modify_grades(self.con, quarter, course_section_id, student, grade)

    def view_course_section_gradesheet(self, quarter = '', course_section_id = '', student = []) -> bool:
        return StudentCourseSection().view_coursesection_gradesheet(self.con, quarter, course_section_id, student)
    
    def add_student_to_coursesection(self, quarter = '', course_section_id = '', student = []):
        return CourseSection().add_student(self.con, quarter, course_section_id, student)
    
    def delete_student_from_coursesection(self, quarter = '', course_section_id = '', student = []):
        return CourseSection().delete_student(self.con, quarter, course_section_id, student)
    
    def add_course_features(self, quarter = '', course_section_id = '', features = []):
        return Modify_Features(self.con, quarter, course_section_id, features).add_features()
    
    def remove_course_features(self, quarter = '', course_section_id = '', features = []):
        return Modify_Features(self.con, quarter, course_section_id, features).remove_features()
    
    def get_course_features(self, quarter = '', course_section_id = ''):
        coursesection = CourseSection()
        results = coursesection.retrieve_course_section(self.con, quarter, course_section_id)
        if results:
            return coursesection.get_course_features()
        else: 
            print("Course Section does not exist!")
            return None
        