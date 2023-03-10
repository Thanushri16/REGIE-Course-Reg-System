# This class creates and populates the database by running the sql script files

from database_connect import *
import os

DATABASE = "course_registration"
HOST = "localhost"
USER = "root"
PASSWORD = "admin"

class DatabaseCreation:
    def create_database(self):
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()

        # Check if the database already exists
        cursor.execute("SHOW DATABASES")
        existing_databases = cursor.fetchall()

        if (DATABASE,) not in existing_databases:
            # Create the new database
            cursor.execute(f"CREATE DATABASE {DATABASE}")
            print("Database created!")
        cursor.close()
        connection.close()

        # Connecting to a new database
        con = Connection.get_instance()
        con = con.connect()
        cursor = con.cursor()
        print("Connected to database!")

        os.chdir(os.path.join(os.path.dirname(os.getcwd()), 'sql'))
        
        for file in os.listdir(os.getcwd()):
            if file.endswith(".sql"):
                with open(os.path.join(os.getcwd(), file), 'r') as f:
                    sql_code = f.read()
                for result in cursor.execute(sql_code, multi=True):
                    pass

        os.chdir(os.path.join(os.path.dirname(os.getcwd()), 'python'))

        print("SQL files executed!")
        con.commit()
        cursor.close()
        con.close()