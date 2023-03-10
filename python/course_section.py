from course import *

class CourseSection:
    def __init__(self, course_section_id=None, quarter_id = None, course_id = None, room_id=None, day = None, start_time = None, end_time = None, permission_required = False) -> None:
        self.__course_section_id = course_section_id
        self.__quarter_id = quarter_id
        self.__course_id = course_id
        self.__faculty = []
        self.__student = []
        self.__room_id = room_id
        self.__current_enrollment = len(self.__student)
        self.__day = day
        self.__start_time = start_time
        self.__end_time = end_time
        self.__permission_required = permission_required
        self.__features = []

    def get_instructors(self): 
        return self.__faculty
    
    def get_students(self):
        return self.__student
    
    def get_quarter_id(self):
        return self.__quarter_id
    
    def get_course_id(self):
        return self.__course_id
    
    def get_course_section_id(self):
        return self.__course_section_id
    
    def get_room_id(self):
        return self.__room_id
    
    def get_current_enrollment(self):
        return self.__current_enrollment
    
    def get_start_time(self):
        return self.__start_time
    
    def get_end_time(self):
        return self.__end_time
    
    def get_course_day(self):
        return self.__day
    
    def get_permission_required_status(self):
        return self.__permission_required
    
    def get_course_features(self):
        return self.__features
    
    def add_course_feature(self, feature):
        self.__features.append(feature)

    def delete_course_feature(self, feature):
        self.__features.remove(feature)

    def set_current_enrollment(self, val):
        self.__current_enrollment = val

    def retrieve_course_section(self, con, quarter, id):
        query = "select * from CourseSection where quarter_id = %s and course_section_id = %s"
        cursor = con.con.cursor()
        cursor.execute(query, (quarter, id))
        results = cursor.fetchone()

        if results: 
            self.__init__(results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7])
            query1 = "select * from StudentCourseSection where quarter_id = %s and course_section_id = %s"
            cursor.execute(query1, (quarter, id))
            results1 = cursor.fetchall()
            for row in results1:
                self.__student.append(int(row[2]))
            self.__current_enrollment = len(self.__student)

            query2 = "select * from FacultyCourseSection where quarter_id = %s and course_section_id = %s"
            cursor.execute(query2, (quarter, id))
            results2 = cursor.fetchall()
            for row in results2:
                self.__faculty.append(int(row[2]))

            query3 = "select * from CourseFeatures where course_section_id = %s"
            cursor.execute(query3, (id,))
            results3 = cursor.fetchall()
            for row in results3:
                self.__features.append(row[1])

            # print("Course section exists")
            cursor.close()
            return (self.__course_section_id, self.__quarter_id, self.__course_id)
        else:
            # print("Course section does not exist")
            cursor.close()
            return None
        

    def get_name_of_coursesection(self, con, quarter='', course_section_id = ''):
        # Function that gets the name of the course the course section is for
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            value = Course().retrieve_course(con, results[2])
            name = value[1]
            # print(f'Name of the course: {name}')
            return name
        else: 
            return None
        
    
    def view_enrolled_students(self, con, quarter = '', course_section_id = ''):
        # This function lets the user to view the enrolled students in a course section
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results: 
            if self.__current_enrollment > 0:
                print("Number of students enrolled in this course are: " + str(self.__current_enrollment))
                return [x for x in self.__student]
            else:
                print("No students are enrolled in this course!")
                return None
        else: 
            print("Course section does not exist")
            return None
        
          
    def add_course_section(self, con) -> bool:
        # This function adds a course section for a course
        # Check if the quarter and the course exists
        results = self.retrieve_course_section(con, self.__quarter_id, self.__course_section_id)
        if not results:
            query = "insert into CourseSection (course_section_id, quarter_id, course_id, room_id, course_day, start_time, end_time, permission_required) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (self.__course_section_id, self.__quarter_id, self.__course_id, self.__room_id, self.__day, self.__start_time, self.__end_time, self.__permission_required)
            cursor = con.con.cursor()
            cursor.execute(query, values)
            con.con.commit()

            cursor.close()
            print("Course section details are added to the database!")
            return True
        else: 
            print("Course section exists already")
            return False
    
        
    def delete_course_section(self, con, quarter='', course_section_id = '') -> bool:
        # This function deletes a course section for a course
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            cursor = con.con.cursor()
            query = "delete from CourseSection where course_section_id = %s and quarter_id = %s"
            cursor.execute(query, (course_section_id, quarter))
            con.con.commit()
            query = "delete from StudentCourseSection where course_section_id = %s and quarter_id = %s"
            cursor.execute(query, (course_section_id, quarter))
            con.con.commit()
            query = "delete from FacultyCourseSection where course_section_id = %s and quarter_id = %s"
            cursor.execute(query, (course_section_id, quarter))
            con.con.commit()
            query = "delete from CourseFeatures where course_section_id = %s"
            cursor.execute(query, (course_section_id, ))
            con.con.commit()
            cursor.close()
            print("Course section deleted")
            return True
        else:
            print("Quarter/Course section does not exist")
            return False

    def delete_course_sections_lessthan5(self, con, quarter='') -> bool:
        # This function deletes course sections with less than 5 students
        query = "select course_section_id, count(student_id) from StudentCourseSection where quarter_id = %s group by course_section_id"
        flag = False
        cursor = con.con.cursor()
        cursor.execute(query, (quarter, ))
        results = cursor.fetchall()
        for row in results: 
            if row[1] < 5:
                query = "delete from CourseSection where course_section_id = %s and quarter_id = %s"
                cursor.execute(query, (row[0], quarter))
                con.con.commit()
                query = "delete from StudentCourseSection where course_section_id = %s and quarter_id = %s"
                cursor.execute(query, (row[0], quarter))
                con.con.commit()
                query = "delete from FacultyCourseSection where course_section_id = %s and quarter_id = %s"
                cursor.execute(query, (row[0], quarter))
                con.con.commit()
                query = "delete from CourseFeatures where course_section_id = %s"
                cursor.execute(query, (row[0], ))
                con.con.commit()
                print(f"Course section {row[0]} deleted!")
                flag = True
        return flag
    

    def add_student(self, con, quarter = '', course_section_id = '', student = []) -> bool:
        # This function adds student to the course section
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            cursor = con.con.cursor()
            for i in student:
                if i not in self.__student:
                    self.__student.append(i)
                    self.__current_enrollment += 1
                    query = "insert into StudentCourseSection (course_section_id, quarter_id, student_id, scores, grade) values(%s,%s,%s,%s,%s)"
                    values = (self.__course_section_id, self.__quarter_id, i, None, None)
                    cursor.execute(query, values)
                    con.con.commit()
                else: 
                    continue
            cursor.close()
            print("Student(s) added!")
            return True

        else:
            print("Quarter/Course section does not exist")
            return False

    def delete_student(self, con, quarter = '', course_section_id = '', student = []) -> bool:
        # This function deletes a student from the course section
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            cursor = con.con.cursor()
            for i in student:
                if i in self.__student:
                    self.__student.remove(i)
                    self.__current_enrollment -= 1
                    query = "delete from StudentCourseSection where course_section_id = %s and quarter_id = %s and student_id = %s"
                    values = (self.__course_section_id, self.__quarter_id, i)
                    cursor.execute(query, values)
                    con.con.commit()
                else: 
                    continue
            cursor.close()
            print("Student(s) deleted!")
            return True
        else:
            print("Quarter/Course section does not exist")
            return False

    def add_instructor(self, con, quarter = '', course_section_id = '', faculty = []) -> bool:
        # This function adds faculty to the course section
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            cursor = con.con.cursor()
            for i in faculty:
                if i not in self.__faculty:
                    self.__faculty.append(i)
                    query = "insert into FacultyCourseSection (course_section_id, quarter_id, faculty_id) values(%s,%s,%s)"
                    values = (self.__course_section_id, self.__quarter_id, i)
                    cursor.execute(query, values)
                    con.con.commit()
                else: 
                    continue
            cursor.close()
            print("Faculty(s) added!")
            return True

        else:
            print("Quarter/Course section does not exist")
            return False

    def delete_instructor(self, con, quarter = '', course_section_id = '', faculty = []) -> bool:
        # This function deletes a faculty from the course section
        # Check if the quarter and the course section exists
        results = self.retrieve_course_section(con, quarter, course_section_id)
        if results:
            cursor = con.con.cursor()
            for i in faculty:
                if i in self.__faculty:
                    self.__faculty.remove(i)
                    query = "delete from FacultyCourseSection where course_section_id = %s and quarter_id = %s and faculty_id = %s"
                    values = (self.__course_section_id, self.__quarter_id, i)
                    cursor.execute(query, values)
                    con.con.commit()
                else: 
                    continue
            cursor.close()
            print("Faculty(s) deleted!")
            return True
        else:
            print("Quarter/Course section does not exist")
            return False