# This file allows a student to register for a course based on the course schedule
# The result that is saved in the database depends on the feature if the course section requires instructor approval or not

from course_section import *
from check_compatibility import *

class RegisterClass:
    def __init__(self, con, student, course_section) -> None:
        self.con = con
        self.student = student
        self.course_section = course_section
        self.check = False
        self.quarter = course_section.get_quarter_id()
        self.compatibility = Check_Compatibility()

    def add_course_to_student(self):
        if self.student.get_id() in self.course_section.get_students():
            print("Student is already registered in the course section!")
            return 
        course_section_schedule2 = [self.course_section.get_course_day(), self.course_section.get_start_time(), self.course_section.get_end_time()]
        course_section_list = self.student.view_registered_course_sections(self.quarter)
        if course_section_list:
            for i in course_section_list:
                course_section_id = i[0]
                quarter_id = i[1]
                coursesection = CourseSection()
                coursesection.retrieve_course_section(self.con, quarter_id, course_section_id)
                course_section_schedule1 = [coursesection.get_course_day(), coursesection.get_start_time(), coursesection.get_end_time()]
                self.check = self.check or self.compatibility.execute(course_section_schedule1, course_section_schedule2)
        if not self.check:
            try: 
                if self.course_section.get_permission_required_status():
                    print("Instructor Permission required to register for this course!")
                    query = "insert into PendingCourseSection values(%s,%s,%s)"
                    cursor = self.con.con.cursor()
                    values = (self.course_section.get_quarter_id(), self.course_section.get_course_section_id(), self.student.get_id())
                    cursor.execute(query, values)
                    self.con.con.commit()
                    cursor.close()
                    print("Your name is added to the pending list of students!")
                else: 
                    self.student.add_course(self.course_section.get_quarter_id(), self.course_section.get_course_section_id())

            except Exception as e:
                print(f"Error in checking checking schedules and adding course section to student: {e}")
        
        return 

