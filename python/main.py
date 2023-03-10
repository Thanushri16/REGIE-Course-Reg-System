from abstract_factory import *
from database_creation import *
from mongodb_database_connect import *
from login import *
from register_class import *
from datetime import date, datetime, timedelta
import uuid
import sys

def main_admin_add_course(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_add_course", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        id = int(input("Enter a course id: "))
        name = input("Enter the course name: ")
        description = input("Enter a description for the course: ")
        fee = int(input("Enter the course fee: "))
        dept_id = None
        while not dept_id:
            dept_name = input("Enter the department name of the dept that offers the course: ")
            
            cursor = admin.con.con.cursor()
            cursor.execute("select * from department where name like %s", (f'%{dept_name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Dept ID\tDept Name")
                for i in results:
                    print(str(i[0])+"\t"+str(i[1]))
                dept_id = int(input("Enter the correct dept_id for the Department from the above list of departments: "))
            else: 
                print("Your dept name does not match with the existing departments! Enter a correct department name!")
                connection.insert_one({"Function": "main_admin_add_course", "Message": "Your dept name does not match with the existing departments! Enter a correct department name!", \
                               "DateTime": datetime.now()})

        if admin.add_course(id, name, description, dept_id, fee):
            print(f"Course {id} is added!")
            connection.insert_one({"Function": "main_admin_add_course", "Message": "Course {id} is added!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course {id} is not added!")
            connection.insert_one({"Function": "main_admin_add_course", "Message": "Course {id} is not added!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_add_course", "Message": "Exiting Function", \
                               "DateTime": datetime.now()})
        return 
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_delete_course(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_delete_course", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("Choose 1 to search based on Course ID or 2 to search based on Course Name!")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            course_id = int(input("Enter a course id (Course ID should be exact): "))

        elif choice == 2:
            course_id = None
            while not course_id:
                name = input("Enter the course name: ")
                cursor = admin.con.con.cursor()
                cursor.execute("select * from course where name like %s", (f'%{name}%',))
                results = cursor.fetchall()
                cursor.close()

                if results:
                    print("Course ID\tCourse Name")
                    for i in results:
                        print(str(i[0])+"\t"+str(i[1]))
                    course_id = int(input("Enter the correct course_id for the course name from the above list of courses: "))
                else: 
                    print("Your course name does not match with the existing courses! Enter a correct course name!")
                    break

        if admin.delete_course(course_id):
            print(f"Course {course_id} is deleted!")
            connection.insert_one({"Function": "main_admin_delete_course", "Message": f"Course {course_id} is deleted!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course {course_id} is not deleted!")
            connection.insert_one({"Function": "main_admin_delete_course", "Message": f"Course {course_id} is not deleted!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_delete_course", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
        
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    
    
def main_admin_modify_course(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_modify_course", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("You cannot modify an ID of the course!")
        course_id = int(input("Enter the course id of the course that you want to modify: "))
        name = input("Enter the course name (Leave blank if you don't want to change): ")
        description = input("Enter a description for the course (Leave blank if you don't want to change): ")
        fee = input("Enter the course fee (Leave blank if you don't want to change): ")
        if fee: 
            fee = int(fee)
        
        dept_name = input("Enter the department name of the dept that offers the course (Leave blank if you don't want to change): ")
        if not dept_name:
            dept_id = None
        else: 
            cursor = admin.con.con.cursor()
            cursor.execute("select * from department where name like %s", (f'%{dept_name}%',))
            results = cursor.fetchall()
            cursor.close()
            dept_id = None

            if results:
                print("Dept ID\tDept Name")
                for i in results:
                    print(str(i[0])+"\t"+str(i[1]))
                dept_id = int(input("Enter the correct dept_id for the Department from the above list of departments: "))
            else: 
                print("Your dept name does not match with the existing departments! Enter a correct department name!")

        if admin.modify_course(course_id, name, description, dept_id, fee):
            print(f"Course {course_id} is modified!")
            connection.insert_one({"Function": "main_admin_modify_course", "Message": f"Course {course_id} is modified!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course {course_id} is not modified!")
            connection.insert_one({"Function": "main_admin_modify_course", "Message": f"Course {course_id} is not modified!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_modify_course", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
        
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_add_student(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_add_student", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        id = int(input("Enter an id: "))
        name = input("Enter the name: ")
        address = input("Enter the address: ")
        mobile = int(input("Enter mobile number: "))
        email = input("Enter email: ")
        password = input("Enter password: ")
        restrictions = input("Enter restrictions (Optional): ")
        advisor = input("Enter the name of the advisor: ")
        gpa = 0     # For a new student, gpa would be zero
        status = input("Enter P for Part-time and F for Full-Time: ")
        if status == "F" or status == "f":
            is_full_time = True
            concentration = input("Enter student concentration: ")
            expected_graduation = input("Enter expected graduation date (yyyy-mm-dd): ")
            dept_id = None
            while not dept_id:
                dept_name = input("Enter the department name of student: ")
                
                cursor = admin.con.con.cursor()
                cursor.execute("select * from department where name like %s", (f'%{dept_name}%',))
                results = cursor.fetchall()
                cursor.close()

                if results:
                    print("Dept ID\tDept Name")
                    for i in results:
                        print(str(i[0])+"\t"+str(i[1]))
                    dept_id = int(input("Enter the correct dept_id for the Department from the above list of departments: "))
                else: 
                    print("Your dept name does not match with the existing departments! Enter a correct department name!")
        elif status == "P" or status == "p":
            is_full_time = False
            concentration = None
            expected_graduation = None
            dept_id = None

        if admin.add_student(id, name, address, mobile, email, password, restrictions, advisor, gpa, is_full_time, dept_id, expected_graduation, concentration):
            print(f"Student {name} is added!")
            connection.insert_one({"Function": "main_admin_add_student", "Message": f"Student {name} is added!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Student {name} is not added!")
            connection.insert_one({"Function": "main_admin_add_student", "Message": f"Student {name} is not added!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_add_student", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_delete_student(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_delete_student", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("Choose 1 to search based on Student ID or 2 to search based on Student Name!")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            student_id = int(input("Enter a student id (Student ID should be exact): "))

        elif choice == 2:
            student_id = None
            while not student_id:
                name = input("Enter the student name: ")
                cursor = admin.con.con.cursor()
                cursor.execute("select * from student where name like %s", (f'%{name}%',))
                results = cursor.fetchall()
                cursor.close()

                if results:
                    print("Student ID\tStudent Name")
                    for i in results:
                        print(str(i[0])+"\t"+str(i[1]))
                    student_id = int(input("Enter the correct student_id for the student name from the above list of students: "))
                else: 
                    print("Your student name does not match with the existing students! Enter a correct student name!")

        if admin.delete_student(student_id):
            print(f"Student {student_id} is deleted!")
            connection.insert_one({"Function": "main_admin_delete_student", "Message": f"Student {name} is deleted!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Student {student_id} is not deleted!")
            connection.insert_one({"Function": "main_admin_delete_student", "Message": f"Student {name} is not deleted!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_delete_student", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
        
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_add_instructor(admin, session, connection): 
    connection.insert_one({"Function": "main_admin_add_instructor", "Message": "Entering function", \
                               "DateTime": datetime.now()})
    if session:
        id = int(input("Enter an id: "))
        name = input("Enter the name: ")
        address = input("Enter the address: ")
        mobile = int(input("Enter mobile number: "))
        email = input("Enter email: ")
        password = input("Enter password: ")
        position = input("Enter position: ")
        status = input("Enter P for Part-time and F for Full-Time: ")
        if status == "F" or status == "f":
            status = "Full-Time"
        elif status == "P" or status == "p":
            status = "Part-Time"
        dept_id = None
        while not dept_id:
            dept_name = input("Enter the department name of faculty: ")
            
            cursor = admin.con.con.cursor()
            cursor.execute("select * from department where name like %s", (f'%{dept_name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Dept ID\tDept Name")
                for i in results:
                    print(str(i[0])+"\t"+str(i[1]))
                dept_id = int(input("Enter the correct dept_id for the Department from the above list of departments: "))
            else: 
                print("Your dept name does not match with the existing departments! Enter a correct department name!")
        
        if admin.add_instructor(id, name, address, mobile, email, password, position, dept_id, status):
            print(f"Faculty {name} is added!")
            connection.insert_one({"Function": "main_admin_add_instructor", "Message": f"Faculty {name} is added!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Faculty {name} is not added!")
            connection.insert_one({"Function": "main_admin_add_instructor", "Message": f"Faculty {name} is not added!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_add_instructor", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_delete_instructor(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_delete_instructor", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("Choose 1 to search based on Instructor ID or 2 to search based on Instructor Name!")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            faculty_id = int(input("Enter a instructor id (Instructor ID should be exact): "))

        elif choice == 2:
            faculty_id = None
            while not faculty_id:
                name = input("Enter the instructor name: ")
                cursor = admin.con.con.cursor()
                cursor.execute("select * from faculty where name like %s", (f'%{name}%',))
                results = cursor.fetchall()
                cursor.close()

                if results:
                    print("Instructor ID\tInstructor Name")
                    for i in results:
                        print(str(i[0])+"\t"+str(i[1]))
                    faculty_id = int(input("Enter the correct faculty_id for the instructor name from the above list of instructors: "))
                else: 
                    print("Your instructor name does not match with the existing instructors! Enter a correct instructor name!")

        if admin.delete_instructor(faculty_id):
            print(f"Instructor {faculty_id} is deleted!")
            connection.insert_one({"Function": "main_admin_delete_instructor", "Message": f"Instructor {faculty_id} is deleted!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Instructor {faculty_id} is not deleted!")
            connection.insert_one({"Function": "main_admin_delete_instructor", "Message": f"Instructor {faculty_id} is not deleted!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_delete_instructor", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
        
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_drop_courses_less_enrollments(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_drop_courses_less_enrollments", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("Deleting courses with less than 5 enrolled students in a particular quarter!")
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = admin.con.con.cursor()
            cursor.execute("select distinct(quarter_id) from CourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name")
                for i in results:
                    print(i[0])
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        if admin.drop_course_sections_lessthan5(quarter_name):
            print("Course Sections with lesser than 5 enrolled students are dropped!")
            connection.insert_one({"Function": "main_admin_drop_courses_less_enrollments", "Message": "Courses dropped!", \
                               "DateTime": datetime.now()})
        else: 
            print("No course sections were dropped!")
            connection.insert_one({"Function": "main_admin_drop_courses_less_enrollments", "Message": "Courses dropped!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_drop_courses_less_enrollments", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_add_course_section(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_add_course_section", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        course_section_id = int(input("Enter the course section id: "))
        quarter_id = input("Enter the quarter ID: ")
        course_id = None
        while not course_id:
            course_name = input("Enter the course name: ")
            
            cursor = admin.con.con.cursor()
            cursor.execute("select * from course where name like %s", (f'%{course_name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Course ID\tCourse Name")
                for i in results:
                    print(str(i[0])+"\t"+str(i[1]))
                course_id = int(input("Enter the correct course_id for the course from the above list of courses: "))
            else: 
                print("Your course name does not match with the existing courses! Enter a correct course name!")
        room_id = int(input("Enter the room id: "))
        day = input("Enter the day of the course section: ")
        start_time = input("Enter the start time of the course section (hh:mm:ss): ")
        end_time = input("Enter the end time of the course section (hh:mm:ss): ")
        permission = input("Enter T if permission is required to add students to this course section and F otherwise: ")
        if permission == "T" or permission == "t":
            permission_required = True
        else:
            permission_required = False

        if admin.add_course_section(course_section_id, quarter_id, course_id, room_id, day, start_time, end_time, permission_required):
            print(f"Course Section {course_section_id} is added!")
            connection.insert_one({"Function": "main_admin_add_course_section", "Message": f"Course Section {course_section_id} is added!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course Section {course_section_id} is not added!")
            connection.insert_one({"Function": "main_admin_add_course_section", "Message": f"Course Section {course_section_id} is not added!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_add_course_section", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_delete_course_section(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_delete_course_section", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = admin.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, course_id from CourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tCourse ID")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        if admin.delete_course_section(course_section_id, quarter_name):
            print(f"Course Section {course_section_id} is deleted!")
            connection.insert_one({"Function": "main_admin_delete_course_section", "Message": f"Course Section {course_section_id} is deleted!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course Section {course_section_id} is not deleted!")
            connection.insert_one({"Function": "main_admin_add_course_section", "Message": f"Course Section {course_section_id} is not deleted!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_delete_course_section", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_add_instructor_to_course_section(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_add_instructor_to_course_section", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = admin.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, course_id from CourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tCourse ID")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        faculty_str = input("Enter instructor IDs of the instructors whom you want to add to the course section (separated by commas if you want to enter multiple values): ")
        faculty = faculty_str.split(",")
        
        if admin.add_instructor_coursesection(course_section_id, quarter_name, faculty):
            print("Instructor has been added to the Course Section!")
            connection.insert_one({"Function": "main_admin_add_instructor_to_course_section", "Message": "Instructor has been added to the Course Section!", \
                               "DateTime": datetime.now()})
        else:
            print("Instructor was not added to the Course Section!")
            connection.insert_one({"Function": "main_admin_add_instructor_to_course_section", "Message": "Instructor was not added to the Course Section!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_add_instructor_to_course_section", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_delete_instructor_from_course_section(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_delete_instructor_from_course_section", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = admin.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, course_id from CourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tCourse ID")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        faculty_str = input("Enter instructor IDs of the instructors whom you want to add to the course section (separated by commas if you want to enter multiple values): ")
        faculty = faculty_str.split(",")

        if admin.delete_instructor_coursesection(course_section_id, quarter_name, faculty):
            print("Instructor has been deleted from the Course Section!")
            connection.insert_one({"Function": "main_admin_delete_instructor_from_course_section", "Message": "Instructor has been deleted from the Course Section!", \
                               "DateTime": datetime.now()})
        else:
            print("Instructor was not deleted from the Course Section!")
            connection.insert_one({"Function": "main_admin_delete_instructor_from_course_section", "Message": "Instructor was not deleted from the Course Section!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_delete_instructor_from_course_section", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return


def main_admin_start_registration(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_start_course_registration", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("Starting course registration!")
        quarter = input("Enter the quarter ID of the quarter for which the course registration is for: ")
        cursor = admin.con.con.cursor()
        cursor.execute("select distinct(quarter_id) from CourseRegistration where quarter_id like %s", (f'%{quarter}%',))
        results = cursor.fetchall()
        cursor.close()

        if not results: 
            cursor = admin.con.con.cursor()
            cursor.execute("insert into CourseRegistration values(%s,%s,%s,%s,%s)",\
                            (f'{quarter}',date.today(),datetime.now().time().strftime("%H:%M:%S"),date.today()+timedelta(days=7),'17:00:00'))
            admin.con.con.commit()
            cursor.close()
            print("Course registration has started!")
            connection.insert_one({"Function": "main_admin_start_course_registration", "Message": "Course registration has started", \
                               "DateTime": datetime.now()})

        else: 
            print("Course registration timings already exist for the given quarter!")
        
        connection.insert_one({"Function": "main_admin_start_course_registration", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_modify_profile(admin, session, connection):
    if session:
        connection.insert_one({"Function": "main_admin_modify_profile", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        print("You cannot modify your admin ID!")
        name = input("Enter the name (Leave blank if you dont want to modify): ")
        address = input("Enter the address (Leave blank if you dont want to modify): ")
        mobile = input("Enter mobile number (Leave blank if you dont want to modify): ")
        if mobile:
            mobile = int(mobile)
        email = input("Enter email (Leave blank if you dont want to modify): ")
        password = input("Enter password (Leave blank if you dont want to modify): ")
        if password: 
            repassword = input("Re enter your password: ")
        else: 
            repassword = None

        if admin.modify_profile(name, address, mobile, email, password, repassword):
            print(f"Admin {admin.get_id() - admin.get_name()} is modified!")
            connection.insert_one({"Function": "main_admin_modify_profile", "Message": f"Admin {admin.get_id() - admin.get_name()} is modified!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Admin {admin.get_id() - admin.get_name()} is not modified!")
            connection.insert_one({"Function": "main_admin_modify_profile", "Message": f"Admin {admin.get_id() - admin.get_name()} is not modified!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_admin_modify_profile", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
        
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    
def main_admin_view_logs(admin, session, connection):
    if session:
        print("Printing Logs: ")
        for row in connection.find({}):
            print(row)
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_admin_clear_logs(admin, session, connection):
    if session:
        connection.delete_many({})
        print("Logs deleted!")
    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def display_admin_menu(user_type, session, id, connection):
    admin = Admin()
    admin.create_connection()
    admin.retrieve_details(id)

    while session: 
        print(f"\nWelcome to your admin page, {admin.get_name()}\n")    

        print("Select task you want to perform:")
        print("Enter 1 to add a course")
        print("Enter 2 to delete a course")
        print("Enter 3 to modify a course")
        print("Enter 4 to add a student")
        print("Enter 5 to delete a student")
        print("Enter 6 to add a instructor")
        print("Enter 7 to delete a instructor")
        print("Enter 8 to drop course sections with lesser enrollments")
        print("Enter 9 to add a course section")
        print("Enter 10 to delete a course section")
        print("Enter 11 to add instructor to a course section")
        print("Enter 12 to delete instructor from a course section")
        print("Enter 13 to start course registration")
        print("Enter 14 to modify profile")
        print("Enter 15 to view logs")
        print("Enter 16 to clear logs")
        print("Enter 17 to log out\n")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            main_admin_add_course(admin, session, connection)
            
        elif choice == 2:
            main_admin_delete_course(admin, session, connection)

        elif choice == 3:
            main_admin_modify_course(admin, session, connection)

        elif choice == 4:
            main_admin_add_student(admin, session, connection)

        elif choice == 5:
            main_admin_delete_student(admin, session, connection)

        elif choice == 6:
            main_admin_add_instructor(admin, session, connection)

        elif choice == 7:
            main_admin_delete_instructor(admin, session, connection)

        elif choice == 8:
            main_admin_drop_courses_less_enrollments(admin, session, connection)

        elif choice == 9:
            main_admin_add_course_section(admin, session, connection)

        elif choice == 10:
            main_admin_delete_course_section(admin, session, connection)

        elif choice == 11:
            main_admin_add_instructor_to_course_section(admin, session, connection)

        elif choice == 12:
            main_admin_delete_instructor_from_course_section(admin, session, connection)

        elif choice == 13:
            main_admin_start_registration(admin, session, connection)

        elif choice == 14:
            main_admin_modify_profile(admin, session, connection)

        elif choice == 15:
            main_admin_view_logs(admin, session, connection)

        elif choice == 16:
            main_admin_clear_logs(admin, session, connection)
        
        elif choice == 17:
            session = None
            return

            
def main_faculty_view_department(faculty, session, connection):
    connection.insert_one({"Function": "main_faculty_view_department", "Message": "Entering function", \
                               "DateTime": datetime.now()})
    print(f"{faculty.view_department_information()}")
    connection.insert_one({"Function": "main_faculty_view_department", "Message": "Exiting function", \
                               "DateTime": datetime.now()})


def main_faculty_view_course_schedule(faculty, session, connection):
    connection.insert_one({"Function": "main_faculty_view_course_schedule", "Message": "Entering function", \
                               "DateTime": datetime.now()})
    course_schedule = faculty.view_current_past_course_schedule()
    print("Course Section ID  Quarter ID")
    for i in course_schedule:
        print(f"{i[1]}          {i[0]}")
    connection.insert_one({"Function": "main_faculty_view_course_schedule", "Message": "Exiting function", \
                               "DateTime": datetime.now()})

def main_faculty_view_all_course_sections(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_view_all_course_sections", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            for val in results:
                cursor = faculty.con.con.cursor()
                cursor.execute("select * from CourseSection where course_section_id = %s and quarter_id = %s",\
                                (val[0], val[1]))
                results1 = cursor.fetchall()
                cursor.execute("select student_id from StudentCourseSection where course_section_id = %s and quarter_id = %s",\
                                (val[0], val[1]))
                results2 = cursor.fetchall()
                students = []
                if results2:
                    students = [x[0] for x in results2]
                cursor.close()
                if results1:
                    print("Course Section ID\tQuarter\tCourse ID\tRoom ID\tDay\tStart Time\tEnd Time\tStudents")
                    for i in results1:
                        print(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}\t{i[5]}\t{i[6]}\t{students}')

        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course sections")
        connection.insert_one({"Function": "main_faculty_view_all_course_sections", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_assign_modify_student_scores(faculty, session, connection):
    if session: 
        connection.insert_one({"Function": "main_faculty_assign_modify_student_scores", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = faculty.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, group_concat(student_id) from StudentCourseSection where quarter_id like %s group by quarter_id, course_section_id", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tStudent IDs")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        student_str = input("Enter student IDs of the students whose scores you want to add/update (separated by commas if you want to enter multiple values): ")
        student = student_str.split(",")

        assignment = int(input("Enter the Assignment number that you want to add/update the score for (1-10): "))
        task = assignment - 1

        score = int(input("Enter the score for the Assignment (0-100): "))

        if faculty.add_modify_student_scores(quarter_name, course_section_id, student, task, score):
            print(f"Score updated to {score}")
            connection.insert_one({"Function": "main_faculty_assign_modify_student_scores", "Message": "Scores updated!", \
                               "DateTime": datetime.now()})
        else: 
            print("Score is not updated!")
            connection.insert_one({"Function": "main_faculty_assign_modify_student_scores", "Message": "Scores not updated!", \
                               "DateTime": datetime.now()})

        connection.insert_one({"Function": "main_faculty_assign_modify_student_scores", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return 
    
    else:
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_assign_modify_student_grades(faculty, session, connection):
    if session: 
        connection.insert_one({"Function": "main_faculty_assign_modify_student_grades", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = faculty.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, group_concat(student_id) from StudentCourseSection where quarter_id like %s group by quarter_id, course_section_id", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tStudent IDs")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        student_str = input("Enter student IDs of the students whose grades you want to add/update (separated by commas if you want to enter multiple values): ")
        student = student_str.split(",")

        print(f"Acceptable grades are {Grades().get_acceptable_grades()}")
        grade = input("Enter the student grade: ")

        if faculty.add_modify_student_grades(quarter_name, course_section_id, student, grade):
            print(f"Grade updated to {grade}")
            connection.insert_one({"Function": "main_faculty_assign_modify_student_grades", "Message": "Grades updated!", \
                               "DateTime": datetime.now()})
        else: 
            print("Grade is not updated!")
            connection.insert_one({"Function": "main_faculty_assign_modify_student_grades", "Message": "Grades not updated!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_faculty_assign_modify_student_grades", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return
    else:
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_view_course_section_gradesheet(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_view_course_section_gradesheet", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = faculty.con.con.cursor()
            cursor.execute("select quarter_id, course_section_id, group_concat(student_id) from StudentCourseSection where quarter_id like %s group by quarter_id, course_section_id", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID\tStudent IDs")
                for i in results:
                    print(f'{i[0]}\t{i[1]}\t{i[2]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        student_str = input("Enter student IDs of the students whose gradesheets you want to view (Optional - gives gradesheets of all students)(separated by commas if you want to enter multiple values): ")
        if student_str:
            student = student_str.split(",")
        else: 
            student = []
        if faculty.view_course_section_gradesheet(quarter_name, course_section_id, student):
            print("Grade disposition sheet displayed!")
        else: 
            print("Grade disposition sheet not displayed!")
        connection.insert_one({"Function": "main_faculty_view_course_section_gradesheet", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return
    else:
        print("You are logged out of the system! Please log in again!")
        return
    

def main_faculty_view_enrolled_students(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_view_enrolled_students", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        course_section_id = None
        while not course_section_id: 
            cursor = faculty.con.con.cursor()
            cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name\tCourse Section ID")
                for i in results:
                    print(f'{i[1]}\t{i[0]}')
                quarter_name = input("Enter the correct quarter_id from the above list: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list of course sections: "))

            else: 
                print("Your quarter name and course_section_id does not match with the existing sections!")

        ans = CourseSection().view_enrolled_students(faculty.con, quarter_name, course_section_id)
        if not ans:
            print(f"Course section {course_section_id} does not have any students!")
        print([student for student in ans])
        connection.insert_one({"Function": "main_faculty_view_enrolled_students", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_add_students_to_coursesection(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_add_students_to_coursesection", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            print("Quarter Name\tCourse Section ID")
            for i in results:
                print(f'{i[1]}\t{i[0]}')
            quarter_name = input("Enter the quarter_id from the above list: ")
            course_section_id = int(input("Enter the correct course_section_id from the above list of course sections to which you want to add students: "))

            student_str = input("Enter student IDs of the students whom you want to add to the course section (separated by commas if you want to enter multiple values): ")
            student = student_str.split(",")
    
            if faculty.add_student_to_coursesection(quarter_name, course_section_id, student):
                print(f"Added students to the course section {course_section_id}")
                connection.insert_one({"Function": "main_faculty_add_students_to_coursesection", "Message": "Students are added to a course section", \
                               "DateTime": datetime.now()})
            else:
                print(f'Could not add students to the course section {course_section_id}')
                connection.insert_one({"Function": "main_faculty_add_students_to_coursesection", "Message": "Students are not added to the course section", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course sections")
        connection.insert_one({"Function": "main_faculty_add_students_to_coursesection", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_delete_students_from_coursesection(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_delete_students_from_coursesection", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            print("Quarter Name\tCourse Section ID")
            for i in results:
                print(f'{i[1]}\t{i[0]}')
            quarter_name = input("Enter the quarter_id from the above list: ")
            course_section_id = int(input("Enter the correct course_section_id from the above list of course sections to which you want to delete students: "))

            student_str = input("Enter student IDs of the students whom you want to delete from the course section (separated by commas if you want to enter multiple values): ")
            student = student_str.split(",")
    
            if faculty.delete_student_from_coursesection(quarter_name, course_section_id, student):
                print(f"Deleted students from the course section {course_section_id}")
                connection.insert_one({"Function": "main_faculty_delete_students_from_coursesection", "Message": "Students deleted from course section", \
                               "DateTime": datetime.now()})
            else:
                print(f'Could not delete students from the course section {course_section_id}')
                connection.insert_one({"Function": "main_faculty_delete_students_from_coursesection", "Message": "Students not deleted from course section", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course sections")
        connection.insert_one({"Function": "main_faculty_delete_students_from_coursesection", "Message": "Exiting function", \
                               "DateTime": datetime.now()})

    else:
        print("You are logged out of the system! Please log in again!")
        return


def main_faculty_add_coursefeatures_to_coursesection(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_add_coursefeatures_to_coursesection", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            print("Quarter Name\tCourse Section ID")
            for i in results:
                print(f'{i[1]}\t{i[0]}')
            quarter_name = input("Enter the quarter_id from the above list: ")
            course_section_id = int(input("Enter the correct course_section_id from the above list of course sections to which you want to delete students: "))
            features_str = input("Enter course features to be added (separated by commas if you want to enter multiple values): ")
            features = features_str.split(",")

            if faculty.add_course_features(quarter_name, course_section_id, features):
                print(f"Features are added to course section {course_section_id}")
            else:
                print(f"Features are not added to course section {course_section_id}")
                
        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course section")
        connection.insert_one({"Function": "main_faculty_add_coursefeatures_to_coursesection", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return
    

def main_faculty_delete_coursefeatures_from_coursesection(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_delete_coursefeatures_from_coursesection", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            print("Quarter Name\tCourse Section ID")
            for i in results:
                print(f'{i[1]}\t{i[0]}')
            quarter_name = input("Enter the quarter_id from the above list: ")
            course_section_id = int(input("Enter the correct course_section_id from the above list of course sections to which you want to delete students: "))
            features_str = input("Enter course features to be removed (separated by commas if you want to enter multiple values): ")
            features = features_str.split(",")

            if faculty.remove_course_features(quarter_name, course_section_id, features):
                print(f"Features are removed from course section {course_section_id}")
            else:
                print(f"Features are not removed from course section {course_section_id}")
                
        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course section")
        connection.insert_one({"Function": "main_faculty_delete_coursefeatures_from_coursesection", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return
    

def main_faculty_view_coursefeatures(faculty, session, connection):
    if session:
        connection.insert_one({"Function": "main_faculty_view_coursefeatures", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        cursor = faculty.con.con.cursor()
        cursor.execute("select course_section_id, quarter_id from FacultyCourseSection where faculty_id = %s", (f'{faculty.get_id()}',))
        results = cursor.fetchall()
        cursor.close()

        if results: 
            print("Quarter Name\tCourse Section ID")
            for i in results:
                print(f'{i[1]}\t{i[0]}')
            quarter_name = input("Enter the quarter_id from the above list: ")
            course_section_id = int(input("Enter the correct course_section_id from the above list of course sections to which you want to delete students: "))
    
            if not faculty.get_course_features(quarter_name, course_section_id):
                print(f"Course section {course_section_id} does not have any features!")
            print([x for x in faculty.get_course_features(quarter_name, course_section_id)])
                
        else: 
            print(f"Faculty {faculty.get_id()} is not associated with any course section")

        connection.insert_one({"Function": "main_faculty_view_coursefeatures", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else:
        print("You are logged out of the system! Please log in again!")
        return


def display_instructor_menu(user_type, session, id, connection):
    faculty = Faculty()
    faculty.create_connection()
    faculty.retrieve_details(id)

    while session: 
        print(f"\nWelcome to your instructor page, {faculty.get_name()}\n")    

        print("Select task you want to perform:")
        print("Enter 1 to view department information")
        print("Enter 2 to view current or past course schedule")
        print("Enter 3 to view current or past course sections with registered students and room assignments")
        print("Enter 4 to add/modify student scores")
        print("Enter 5 to add/modify student grades")
        print("Enter 6 to view course section grade disposition spreadsheet")
        print("Enter 7 to view enrolled students in a course section")
        print("Enter 8 to add students to a course section")
        print("Enter 9 to delete students from a course section")
        print("Enter 10 to add course features to a course section")
        print("Enter 11 to delete course features from a course section")
        print("Enter 12 to view course section features")
        print("Enter 13 to log out\n")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            main_faculty_view_department(faculty, session, connection)

        elif choice == 2:
            main_faculty_view_course_schedule(faculty, session, connection)

        elif choice == 3:
            main_faculty_view_all_course_sections(faculty, session, connection)

        elif choice == 4:
            main_faculty_assign_modify_student_scores(faculty, session, connection)

        elif choice == 5:
            main_faculty_assign_modify_student_grades(faculty, session, connection)

        elif choice == 6:
            main_faculty_view_course_section_gradesheet(faculty, session, connection)

        elif choice == 7:
            main_faculty_view_enrolled_students(faculty, session, connection)

        elif choice == 8:
            main_faculty_add_students_to_coursesection(faculty, session, connection)

        elif choice == 9:
            main_faculty_delete_students_from_coursesection(faculty, session, connection)

        elif choice == 10:
            main_faculty_add_coursefeatures_to_coursesection(faculty, session, connection)

        elif choice == 11:
            main_faculty_delete_coursefeatures_from_coursesection(faculty, session, connection)   

        elif choice == 12:
            main_faculty_view_coursefeatures(faculty, session, connection) 

        elif choice == 13:
            session = None
            return
        

def main_student_view_all_course_sections_offered(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_view_all_course_sections_offered", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = student.con.con.cursor()
            cursor.execute("select distinct(quarter_id) from CourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name")
                for i in results:
                    print(i[0])
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        if not student.view_all_course_sections(quarter_name):
            print("No course sections are offered for this quarter")
        else: 
            print("Course Section ID\tQuarter ID\tCourse ID\tCourse Name\tRoom ID\tDay\tStart Time\tEnd Time")
            for x in student.view_all_course_sections(quarter_name):
                print(f"{x[0]}\t{x[1]}\t{x[2]}\t{x[3]}\t{x[4]}\t{x[5]}\t{x[6]}\t{x[7]}")
        connection.insert_one({"Function": "main_student_view_all_course_sections_offered", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_student_register_course(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_register_course", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        
        # Get Quarter Name
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = student.con.con.cursor()
            cursor.execute("select distinct(quarter_id) from CourseRegistration where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Quarter Name")
                for i in results:
                    print(i[0])
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        # Check if the registration is open or closed
        cursor = student.con.con.cursor()
        cursor.execute("select * from CourseRegistration where quarter_id = %s", (f'{quarter_name}',))
        results = cursor.fetchone()
        cursor.close()
        if results:
            start_date_string = results[1].strftime("%Y-%m-%d")
            end_date_string = results[3].strftime("%Y-%m-%d")
            start = datetime.strptime(start_date_string + " " + str(results[2]), "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_date_string + " " + str(results[4]), "%Y-%m-%d %H:%M:%S")
            current = datetime.now()
            if not start <= current <=  end:
                print("Course registration has not started or has already ended! You cannot register for your courses now!")
                return
            
            # View all the courses offered in the current quarter for scheduling
            main_student_view_all_course_sections_offered(student, session, connection)

            # Retrieve course section object
            quarter_id = input("Enter quarter ID: ")
            course_section_id = int(input("Enter course section ID: "))
            course_section = CourseSection()
            course_section.retrieve_course_section(student.con, quarter_id, course_section_id)

            # Register for course section
            RegisterClass(student.con, student, course_section).add_course_to_student()
            
        else: 
            print("Course registration timings are not set up! You cannot register for your courses now!")

        connection.insert_one({"Function": "main_student_register_course", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_student_drop_course(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_drop_course", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        
        main_student_view_registered_course_sections_for_quarter(student, session, connection)
        quarter_id = input("Enter the correct quarter ID from the above list: ")
        course_section_id = int(input("Enter the course section ID of the section you want to delete from the above list"))
        if student.delete_course(quarter_id, course_section_id):
            print(f"Course section {course_section_id} is dropped!")
            connection.insert_one({"Function": "main_student_drop_course", "Message": f"Course section {course_section_id} is dropped!", \
                               "DateTime": datetime.now()})
        else: 
            print(f"Course section {course_section_id} is not dropped!")
            connection.insert_one({"Function": "main_student_drop_course", "Message": f"Course section {course_section_id} is not dropped!", \
                               "DateTime": datetime.now()})
        connection.insert_one({"Function": "main_student_drop_course", "Message": "Exiting function", \
                               "DateTime": datetime.now()})

    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_student_view_course_grades(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_view_course_grades", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = student.con.con.cursor()
            cursor.execute("select distinct course_section_id, quarter_id from StudentCourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Course Section ID\tQuarter Name")
                for i in results:
                    print(f'{i[0]}\t{i[1]}')
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
                course_section_id = int(input("Enter the correct course_section_id from the above list: "))
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        if not student.view_course_section_grade(quarter_name, course_section_id):
            print("No course section grades exist")
        else: 
            print("Course Section grade exists")
        connection.insert_one({"Function": "main_student_view_course_grades", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_student_print_transcripts(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_print_transcripts", "Message": "Entering function", \
                               "DateTime": datetime.now()})

        if student.print_transcript():
            print("Transcript is displayed!")
        else: 
            print("Transcript is not displayed!")
        connection.insert_one({"Function": "main_student_print_transcripts", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return


def main_student_view_gpa(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_view_gpa", "Message": "Entering function", \
                               "DateTime": datetime.now()})

        print(f"GPA: {student.gpa()}")
        connection.insert_one({"Function": "main_student_view_gpa", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_student_view_registered_course_sections_for_quarter(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_view_registered_course_sections_for_quarter", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = student.con.con.cursor()
            cursor.execute("select distinct course_section_id, quarter_id from StudentCourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Course Section ID\tQuarter Name")
                for i in results:
                    print(f'{i[0]}\t{i[1]}')
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        if not student.view_registered_course_sections(quarter_name):
            print("No course sections registered by student")
        else: 
            print("Course Section ID\tQuarter ID\tCourse Name")
            for x in student.view_registered_course_sections(quarter_name):
                print(f"{x[0]}\t{x[1]}\t{x[2]}")
        connection.insert_one({"Function": "main_student_view_registered_course_sections_for_quarter", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def main_student_view_number_of_registered_course_section_for_quarter(student, session, connection):
    if session:
        connection.insert_one({"Function": "main_student_view_number_of_registered_course_section_for_quarter", "Message": "Entering function", \
                               "DateTime": datetime.now()})
        quarter_name = None
        while not quarter_name:
            name = input("Enter the quarter name: ")
            cursor = student.con.con.cursor()
            cursor.execute("select distinct course_section_id, quarter_id from StudentCourseSection where quarter_id like %s", (f'%{name}%',))
            results = cursor.fetchall()
            cursor.close()

            if results:
                print("Course Section ID\tQuarter Name")
                for i in results:
                    print(f'{i[0]}\t{i[1]}')
                quarter_name = input("Enter the correct quarter name from the above list of quarters: ")
            else: 
                print("Your quarter name does not match with the existing quarters! Enter a correct quarter name!")

        print("Number of courses registered: ", student.view_number_of_registered(quarter_name))
        connection.insert_one({"Function": "main_student_view_number_of_registered_course_section_for_quarter", "Message": "Exiting function", \
                               "DateTime": datetime.now()})
        return

    else: 
        print("You are logged out of the system! Please log in again!")
        return
    

def get_student_status(user_type, session, id, connection):
    student = Student()
    student.create_connection()
    query = "select * from student where id = %s"
    cursor = student.con.con.cursor()
    cursor.execute(query, (id,))
    results = cursor.fetchone()
    if results:
        status = results[9]
    else:
        status = None
    if status == 1:
        fulltimestudent = FullTimeStudent()
        fulltimestudent.create_connection()
        fulltimestudent.retrieve_full_time_details(id)
        connection.insert_one({"Function": "get_student_status", "Message": "User is a Full Time Student", \
                               "DateTime": datetime.now()})
        return fulltimestudent

    elif status == 0:
        parttimestudent = PartTimeStudent()
        parttimestudent.create_connection()
        parttimestudent.retrieve_part_time_details(id)
        connection.insert_one({"Function": "get_student_status", "Message": "User is a Part Time Student", \
                               "DateTime": datetime.now()})
        return parttimestudent

    elif status == None:
        print("Student does not exist!")
        connection.insert_one({"Function": "get_student_status", "Message": "User does not exist in Student database", \
                               "DateTime": datetime.now()})
        return 

def display_student_menu(user_type, session, id, connection):
    
    student = get_student_status(user_type, session, id, connection)
    if not student:
        return

    while session: 
        print(f"\nWelcome to your student page, {student.get_name()}\n")    
        student.create_connection()
        print("Select task you want to perform:")
        print("Enter 1 to view all the course sections offered in a quarter")
        print("Enter 2 to register for a course")
        print("Enter 3 to drop a course")
        print("Enter 4 to view course grades")
        print("Enter 5 to print transcripts")
        print("Enter 6 to view their gpa")
        print("Enter 7 to view their registered course sections for the quarter")
        print("Enter 8 to view the number of course sections they registered for the quarter")
        print("Enter 9 to log out\n")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            main_student_view_all_course_sections_offered(student, session, connection)

        elif choice == 2:
            main_student_register_course(student, session, connection)

        elif choice == 3:
            main_student_drop_course(student, session, connection)

        elif choice == 4:
            main_student_view_course_grades(student, session, connection)

        elif choice == 5:
            main_student_print_transcripts(student, session, connection)

        elif choice == 6:
            main_student_view_gpa(student, session, connection)

        elif choice == 7:
            main_student_view_registered_course_sections_for_quarter(student, session, connection)

        elif choice == 8:
            main_student_view_number_of_registered_course_section_for_quarter(student, session, connection)

        elif choice == 9:
            session = None
            return

def main():
    '''
    This function displays the main menu of the REGIE Course Registration System
    '''
    # Create the database
    DatabaseCreation().create_database()

    # Creating MongoDB database for logging
    con_mongo = Mongo_Database.get_instance()
    connection = con_mongo.connect()

    print("Welcome to REGIE Course Registration System!")
    print("Enter 1 to login!")
    print("Enter 2 to Exit!")
    option = int(input("Enter your option: "))

    while option == 1:

        id = int(input("Enter your user id: "))
        password = input("Enter your password: ")
        user_type = Login().login(id, password)
        if user_type:
            session = str(uuid.uuid4())
            if user_type == "admin":
                display_admin_menu(user_type, session, id, connection)
            elif user_type == "faculty":
                display_instructor_menu(user_type, session, id, connection)
            elif user_type == "student": 
                display_student_menu(user_type, session, id, connection)
            
        else:
            print("Incorrect User ID or Password!")

        option = int(input("Enter 1 to Login again or 2 to Exit! What is your choice? "))

    print("Thank you for using the REGIE course registration system!")
    con_mongo.close()
    sys.exit()
    

if __name__ == "__main__":
    main()