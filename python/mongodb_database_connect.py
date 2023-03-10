# Concepts implemented: Abstraction, Interface segregation and Singleton pattern
# Connector methods are created in a separate class to maintain Dependency inversion 
# Other classes don't have to know about the connection details. They just require the connection  object. 

from abc import ABC, abstractmethod
import pymongo

DATABASE = "course_registration"
HOST = "localhost"
COLLECTION = "REGIE_logging"
CONNECTION_STRING = "mongodb://localhost:27017"

class Mongo_Database_Interface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

class Mongo_Database(Mongo_Database_Interface):
    # This private instance variable holds the reference to the single instance of the class
    __instance = None

    def __init__(self):
        # The config is a private variable.
        # However, the connection that is going to be returned is a public connection object
        self.__connection_string = CONNECTION_STRING

    @classmethod
    def get_instance(cls):
        # This class method implements the concept of singleton pattern
        # This method checks if an instance of the class has already been created.
        # Creates a connection instance only if the instance is empty. Returns the existing instance otherwise.
        if not cls.__instance:
            print("Creating a new mongodb database connection instance!")
            cls.__instance = Mongo_Database()
        return cls.__instance

    def connect(self):
        # This function creates the database connection with the connection details in the constructor and returns the connection object
        try: 
            self.client = pymongo.MongoClient(self.__connection_string)
            if DATABASE not in self.client.list_database_names():
                #
                print(f"Database {DATABASE} created in MongoDB!")
            else: 
                self.database = self.client[DATABASE]
                print(f"Database {DATABASE} already exists in MongoDB!")
                
            print("Connected to MongoDB database!")
            if COLLECTION not in self.database:
                #
                print(f"Collection {COLLECTION} created!")
            else: 
                self.collection = self.database[COLLECTION]
                print(f"Collection {COLLECTION} already exists!")
            Mongo_Database.__instance = self
            return self
        except Exception as e:
            print(f'Error in connecting to mongodb database: {e}')

    def get_db(self):
        return self.database
    
    def get_collection(self):
        return self.collection
    
    def close(self):
        # This function closes the database connection if it is open
        try: 
            self.database.client.close()
            print("Connection to MongoDB database closed!")
        except Exception as e:
            print(str(e))


connection = Mongo_Database.get_instance()
print(connection.connect())
db = connection.get_db()
collection = connection.get_collection()
print(db, collection)

# Close the connection to the database
connection.close()