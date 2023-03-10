# This class implements the composite design pattern where to assign a student grade
# it takes the student_id, course_section_id, grade and sets the grade if the student 
# is registered in the course. 

# A faculty can assign grade to a group of students or a single student by calling 
# the same event function that demonstrates the concept of function
# overloading or polymorphism. 

from grades import Grades
from course_section import CourseSection

class Assign_Grade: 
    def __init__(self, con, quarter, course_section_id, student, grade) -> None:
        self.__con = con
        self.__quarter = quarter
        self.__course_section_id = course_section_id
        self.__student = student
        self.__grade = grade

    # Execute operation for both single or multi student grade assignments
    def event(self):
        if len(self.__student) == 1:
            return self.leaf()
        else: 
            return self.composite()

    def leaf(self):
        if self.__grade in Grades().get_acceptable_grades():
            if self.__student[0] in CourseSection().view_enrolled_students(self.__con, self.__quarter, self.__course_section_id):
                cursor = self.__con.con.cursor()
                query = "update StudentCourseSection set grade = %s where quarter_id = %s and course_section_id = %s and student_id = %s"
                values = (self.__grade, self.__quarter, self.__course_section_id, self.__student[0])
                cursor.execute(query, values)
                self.__con.con.commit()
                cursor.close()
                print(f"Grade updated to {self.__grade} for student {self.__student[0]}!")
                return True
            else: 
                print("Student is not there in the course section!")
                return False
        else: 
            print("Grade is not acceptable!")
            return False
        
    def composite(self):
        if self.__grade in Grades().get_acceptable_grades():
            for i in self.__student:
                if i in CourseSection().view_enrolled_students(self.__con, self.__quarter, self.__course_section_id):
                    cursor = self.__con.con.cursor()
                    query = "update StudentCourseSection set grade = %s where quarter_id = %s and course_section_id = %s and student_id = %s"
                    values = (self.__grade, self.__quarter, self.__course_section_id, self.__student[0])
                    cursor.execute(query, values)
                    self.__con.con.commit()
                    cursor.close()
                    print(f"Grade updated to {self.__grade} for student {i}!")
                else: 
                    print("Student is not enrolled in the course section!")
                    return False
        else: 
            print("Grade is not acceptable!")
            return False

    

        