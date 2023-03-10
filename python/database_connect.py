# Concepts implemented: Abstraction, Interface segregation and Singleton pattern
# Connector methods are created in a separate class to maintain Dependency inversion 
# Other classes don't have to know about the connection details. They just require the connection  object. 

from abc import ABC, abstractmethod
import mysql.connector
from mysql.connector import errorcode

DATABASE = "course_registration"
HOST = "localhost"
USER = "root"
PASSWORD = "admin"

class ConnectionInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

class Connection(ConnectionInterface):
    # This private instance variable holds the reference to the single instance of the class
    __instance = None

    def __init__(self):
        # The config is a private variable.
        # However, the connection that is going to be returned is a public connection object
        self.__config = {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,
        'database': DATABASE
        }
        self.con = None

    @classmethod
    def get_instance(cls):
        # This class method implements the concept of singleton pattern
        # This method checks if an instance of the class has already been created.
        # Creates a connection instance only if the instance is empty. Returns the existing instance otherwise.
        if not cls.__instance:
            print("Creating a new database connection instance!")
            cls.__instance = Connection()
        return cls.__instance

    def connect(self):
        # This function creates the database connection with the connection details in the constructor and returns the connection object
        try: 
            self.con = mysql.connector.connect(**self.__config)
            if self.con.is_connected():
                print("Connected to MySQL database!")
            return self.con
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        # This function closes the database connection if it is open
        try: 
            if self.con: 
                self.con.close()
                print("Connection to MySQL database closed!")
            else:
                print("No database connection exists!")
        except Exception as e:
            print(str(e))

# if __name__ == "__main__":
#     # This case creates a new instance
#     con = Connection.get_instance("localhost","root","admin","course_registration")
#     con.connect()
#     print(con.__class__)
#     print(con.con.__class__)
#     con.close()

#     # This case returns an existing instance
#     con2 = Connection.get_instance("localhost","root","admin","course_registration")
#     con2.connect()
#     print(con2.__class__)
#     print(con2.con.__class__)
#     con2.close()