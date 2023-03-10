from student import *
from database_connect import *

# Concrete Full-Time Student Class that inherits Student class
class FullTimeStudent(Student):
    def __init__(self, id, name, address, mobile, email, password, restrictions, advisor, gpa, \
        dept_id = '', expected_graduation = '', concentration = '') -> None:
        self.dept_id = dept_id
        self.expected_graduation = expected_graduation
        self.concentration = concentration
        super().__init__(id, name, address, mobile, email, password, restrictions, advisor, gpa, True)

    def get_student_status(self):
        return "Full-Time student"
    
    def initialize_details(self):
        # This function persists the admin details in the database
        query = "insert into Student (id, name, address, mobile, email, password, restrictions, advisor, gpa, status, dept_id, expected_graduation, concentration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (self._id, self._name, self._address, self._mobile, self._email, self._password, self._restrictions, self._advisor, self._gpa, True, self.dept_id, self.expected_graduation, self.concentration)
        cursor = self.con.con.cursor()
        cursor.execute(query, values)
        self.con.con.commit()
        cursor.close()

    def retrieve_details(self, id):
        query = "select * from student where id = %s"
        cursor = super().con.con.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        if results:
            super().__init__(results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7], results[8], results[9])
            self.dept_id = results[10]
            self.expected_graduation = results[11] 
            self.concentration = results[12]
            return self.get_name()
        else:
            return None