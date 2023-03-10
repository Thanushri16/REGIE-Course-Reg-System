from student import *

# Concrete Part-Time Student Class that inherits Student class
class PartTimeStudent(Student):
    def __init__(self, id, name, address, mobile, email, password, restrictions, advisor, gpa) -> None:
        super().__init__(id, name, address, mobile, email, password, restrictions, advisor, gpa, False)

    def get_student_status(self):
        return "Part-Time student"
    
    def initialize_details(self):
        # This function persists the admin details in the database
        query = "insert into Student (id, name, address, mobile, email, password, restrictions, advisor, gpa, status, dept_id, expected_graduation, concentration) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (self._id, self._name, self._address, self._mobile, self._email, self._password, self._restrictions, self._advisor, self._gpa, True, None, None, None)
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
            return self.get_name()
        else:
            return None