from user import *
from course_section import *
from student_course_section import *
from database_connect import *

# Concrete Student Class
class Student(User):
    def __init__(self, id='', name='', address='', mobile='', email='', password='', restrictions='', advisor='', gpa='', is_full_time='') -> None:
        super().__init__(id, name, address, mobile, email, password)
        self._restrictions = restrictions
        self._advisor = advisor
        self._gpa = gpa
        self._is_full_time = is_full_time
        self.con = None

    def get_type(self):
        return "Student"

    def get_restrictions(self):
        return self._restrictions

    def get_advisor(self) -> str:
        return self._advisor

    def get_gpa(self) -> float:
        return self._gpa

    def set_restrictions(self, val) -> bool:
        self._restrictions = val
        return True

    def set_advisor(self, val) -> bool:
        if len(val) > 0:
            self._advisor = val
            return True
        return False

    def set_gpa(self, val) -> bool:
        self._gpa = val
        return True

    def change_student_status(self):
        if self._is_full_time:
            self._is_full_time = False
        else:
            self._is_full_time = True
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

    def retrieve_status(self, id):
        query = "select * from student where id = %s"
        cursor = super().con.con.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        if results:
            return results[9]
        else:
            return None

    def modify_profile(self, id, name='', address='', mobile='', email='', password='', repassword='', restrictions='', advisor='', gpa='') -> bool:
        flag = False
        d = {}
        if name or address or mobile or email or password or repassword:
            d = super().modify_profile(name, address, mobile, email, password, repassword)
            flag = True
        if restrictions:
            flag = self.set_restrictions(restrictions)
            d["restrictions"] = restrictions
        if advisor: 
            flag = self.set_advisor(advisor)
            d["advisor"] = advisor
        if gpa: 
            flag = self.set_gpa(gpa)
            d["gpa"] = gpa
        if flag:
            print("Changes made to student profile")
        return d
    
    def add_course(self, quarter = '', course_section_id = '') -> bool:
        return CourseSection().add_student(self.con, quarter, course_section_id, [self.get_id()]) and \
            StudentCourseSection(course_section_id, quarter, self.get_id())

    def delete_course(self, quarter = '', course_section_id = '') -> bool:
        return CourseSection().delete_student(self.con, quarter, course_section_id, [self.get_id()]) 

    def view_course_section_grade(self, quarter = '', course_section_id = '') -> bool:
        return StudentCourseSection().view_coursesection_gradesheet(self.con, quarter, course_section_id, [self.get_id()])

    def print_transcript(self) -> bool:
        return StudentCourseSection().print_transcript(self.con, self.get_id())
    
    def view_all_course_sections(self, quarter):
        query = "select * from CourseSection where quarter_id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (quarter, ))
        results = cursor.fetchall()
        if results: 
            course_sections = []
            for x in results:
                name = CourseSection().get_name_of_coursesection(self.con, quarter=x[1], course_section_id = x[0])
                course_sections.append([x[0], x[1], x[2], name, x[3], x[4], x[5], x[6]]) 
            return course_sections
        else:
            return None
        
    def gpa(self): 
        gpa = StudentCourseSection().calculate_avg_gpa(self.con, student_id = self.get_id())
        self.set_gpa(gpa)
        return gpa

    def view_registered_course_sections(self, quarter): 
        query = "select * from StudentCourseSection where student_id = %s and quarter_id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (self.get_id(), quarter))
        results = cursor.fetchall()
        if results: 
            course_sections = []
            for x in results:
                name = CourseSection().get_name_of_coursesection(self.con, quarter=x[0], course_section_id = x[1])
                course_sections.append([x[1], x[0], name]) 
            return course_sections
        else:
            return None
        
    def view_number_of_registered(self, quarter):
        query = "select * from StudentCourseSection where student_id = %s and quarter_id = %s"
        cursor = self.con.con.cursor()
        cursor.execute(query, (self.get_id(), quarter))
        results = cursor.fetchall()
        return len(results)