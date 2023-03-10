from department import *

class Course:
    def __init__(self, id=None, name=None, description=None, dept_id=None, fee=None) -> None:
        self.__id = id
        self.__name = name
        self.__description = description
        self.__dept_id = dept_id
        self.__fee = fee

    def get_course_id(self):
        return self.__id

    def get_course_name(self):
        return self.__name

    def get_course_description(self):
        return self.__description

    def get_dept_info(self, con):
        query = "select * from department where id = %s"
        cursor = con.con.cursor()
        cursor.execute(query, (self.__dept_id,))
        results = cursor.fetchone()
        cursor.close()
        if results:
            d = Department(results[0], results[1], results[3], results[2])
            return d.get_dept_name()
        else:
            return None

    def get_fee(self):
        return self.__fee

    def set_course_description(self, val):
        if val != self.__description:
            self.__description = val
            return True
        return False

    def set_dept_id(self, val):
        if val != self.__dept_id:
            self.__dept_id = val
            return True
        return False

    def set_fee(self, val):
        if val != self.__fee:
            self.__fee = val
            return True
        return False

    def retrieve_course(self, con, id):
        query = "select * from course where id = %s"
        cursor = con.con.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        cursor.close()
        return results

    def add_course(self, con) -> bool:
        # Function that adds a course in the course database if the course id of the course does not exist in the table previously
        results = self.retrieve_course(con, self.__id)
        if results:
            print("Course already exists!")
            return False
        else:
            query = "insert into course (id, name, description, dept_id, fee) values (%s,%s,%s,%s,%s)"
            values = (self.__id, self.__name, self.__description, self.__dept_id, self.__fee)
            cursor = con.con.cursor()
            cursor.execute(query, values)
            con.con.commit()
            cursor.close()
            print("Course added to the course database")
            return True

    def delete_course(self, con, id) -> bool:
        # Function that deletes a course in the course database
        results = self.retrieve_course(con, id)
        if results:
            cursor = con.con.cursor()
            query = "delete from course where id = %s"
            cursor.execute(query, (id,))
            con.con.commit()
            cursor.close()
            print("Course deleted!")
            return True
        else: 
            print("Course doesn't exist")
            return False

    def modify_course_details(self, con, id, name='', description='', dept_id='', fee='') -> bool:
        # Function that modifies the course details in the course database
        results = self.retrieve_course(con, id)
        if not results:
            print("Course doesn't exist!")
            return False
        flag = 0
        
        d = {}
        if len(name) > 0 and results[1] != name:
            # No changes are to be made unless the new value is different from the old value and the new value is not empty
            d["name"] = name
            flag = 1
        if len(description) > 0 and results[2] != description:
            d["description"] = description
            flag = 1
        if dept_id and results[3] != dept_id:
            d["dept_id"] = dept_id
            flag = 1
        if fee and results[4] != fee:
            d["fee"] = fee
            flag = 1
                
        if flag: 
            cursor = con.con.cursor()
            for key, value in d.items():
                query = "update course set " + key + " = %s where id = %s"
                values = (value, id)
                cursor.execute(query, values)
                con.con.commit()
            cursor.close()
            print("Changes made to the course")
            return True
        else: 
            print("No changes made")
            return False