from database_connect import *
import pytest

@pytest.fixture(scope="module")
def db_connect():
    con = Connection.get_instance()
    con.connect()
    yield con
    
@pytest.fixture(scope="module")
def db_close():
    con = Connection.get_instance()
    con.connect()
    con.close()
    yield con
    
def test_connect(db_connect):
    assert (db_connect.con.is_connected() and isinstance(db_connect.con, mysql.connector.connection.MySQLConnection)) == True

def test_close(db_close):
    assert db_close.con.is_connected() == False

# Code that can be used to test query execution (this will be required later)
# def test_query_execution(db_connect):
#     cursor = db_connect.con.cursor()
#     query = "SELECT * FROM student"
#     cursor.execute(query)
#     result = cursor.fetchall()
#     assert len(result) > 0