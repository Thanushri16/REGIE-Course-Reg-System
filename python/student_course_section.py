from assign_grade import *

class StudentCourseSection:
    def __init__(self, course_section_id=None, quarter_id = None, student_id = None, scores = [], grade = '') -> None:
        self.__course_section_id = course_section_id
        self.__quarter_id = quarter_id
        self.__student_id = student_id
        self.__scores = scores
        self.__grade = grade

    def get_course_section_id(self):
        return self.__course_section_id
    
    def get_quarter_id(self):
        return self.__quarter_id
    
    def get_student_id(self):
        return self.__student_id
    
    def get_scores(self):
        return self.__scores
    
    def get_grade(self):
        return self.__grade

    def assign_or_modify_scores(self, con, quarter='', course_section_id='', student = [], task = '', score = 0) -> bool: 
        # Assign or modify scores for students
        cursor = con.con.cursor()
        for i in student:
            query = "select scores from StudentCourseSection where quarter_id = %s and course_section_id = %s and student_id = %s"
            cursor.execute(query, (quarter, course_section_id, i))
            results = cursor.fetchone()
            if results: 
                score_list = str(results[0]).split(',')
                score_list[task] = score
                score_values = str(','.join([str(x) for x in score_list]))
                query = "update StudentCourseSection set scores = %s where quarter_id = %s and course_section_id = %s and student_id = %s"
                values = (score_values, quarter, course_section_id, i)
                cursor.execute(query, values)
                con.con.commit()
                cursor.close()
                print(f"Score updated to {score}!")
                return True
            else:
                cursor.close()
                print("Student does not exist!")
                return False

    def assign_or_modify_grades(self, con, quarter='', course_section_id='', student = [], grade = '') -> bool:
        # Assign or modify grades for students
        return Assign_Grade(con, quarter, course_section_id, student, grade).event()
            
    def view_coursesection_gradesheet(self, con, quarter='', course_section_id='', student = []) -> bool:
        # Try doing for multiple students in a list
        # View gradesheet of a student in a course or for the entire class in the course
        if len(student) > 0: 
            cursor = con.con.cursor()
            for i in student: 
                query = "select * from StudentCourseSection where quarter_id = %s and course_section_id = %s and student_id = %s"
                cursor.execute(query, (quarter, course_section_id, i))
                i = cursor.fetchone()
                print("Course Section gradesheet:")
                print("Course Section ID\tQuarter ID\tStudent ID\tScores\tGrade")
                print(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}')
            cursor.close()
            return True
        else:
            cursor = con.con.cursor()
            query = "select * from StudentCourseSection where quarter_id = %s and course_section_id = %s"
            cursor.execute(query, (quarter, course_section_id))
            results = cursor.fetchall()
            if results:
                print("Course Section gradesheet:")
                print("Course Section ID\tQuarter ID\tStudent ID\tScores\tGrade")
                for i in results: 
                    print(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}')
                cursor.close()
                return True
            else: 
                print("Course section is not registered")
                return False
        

    def calculate_avg_gpa(self, con, student_id = '') -> bool:
        # Function that calculates gpa of student(s)
        cursor = con.con.cursor()
        query = "select grade from StudentCourseSection where student_id = %s"
        cursor.execute(query, (student_id, ))
        results = cursor.fetchall()
        cursor.close()
        if not results:
            print("GPA can't be calculated! Zero course sections registered by the student")
            return False
        else:
            total = 0
            for i in results:
                grade_dict = Grades().get_gpa_point_scale()
                total += grade_dict[i[0]]
            gpa = total/len(results)
            print(f"GPA of student {student_id}: {gpa}")
            return gpa

    def print_transcript(self, con, student_id = '') -> bool:
        # Function that prints transcript for a student
        cursor = con.con.cursor()
        query = "select * from StudentCourseSection where student_id = %s"
        cursor.execute(query, (student_id, ))
        results = cursor.fetchall()
        cursor.close()
        if not results:
            print("Zero course sections registered by the student")
            return False
        else:
            print("Transcript:")
            print("Course Section ID\tQuarter ID\tStudent ID\tGrade")
            for i in results: 
                print(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[4]}')
            cursor.close()
            return True