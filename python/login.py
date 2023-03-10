from database_connect import *

class Login: 
    def __init__(self) -> None:
        pass

    def login(self, id, password):
        con = Connection.get_instance()
        con = con.connect()
        cursor = con.cursor()

        query = "select * from admin where id = %s and password = %s"
        cursor.execute(query, (id,password))
        results = cursor.fetchone()
        
        if results: 
            cursor.close()
            return "admin"
        
        query = "select * from faculty where id = %s and password = %s"
        cursor.execute(query, (id,password))
        results = cursor.fetchone()
        
        if results: 
            cursor.close()
            return "faculty"
        
        query = "select * from student where id = %s and password = %s"
        cursor.execute(query, (id,password))
        results = cursor.fetchone()
        
        if results: 
            cursor.close()
            return "student"

        cursor.close()
        return None