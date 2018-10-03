import  mysql.connector

from .config     import *
import cgiutils

current_connection = None

# Connect to the database and return the connection object
# If an error occurs, a 500 HTTP response will be printed
# and the script will immediately exit
#
# If there is already a current connection, that connection will
# be closed and replaced with this one
def connect():
    global current_connection
    if current_connection is not None:
        current_connection.close()
        current_connection = None
    try:
        conn = mysql.connector.connect(
            user        = MYSQL_USER,
            password    = MYSQL_PASSWORD,
            host        = MYSQL_HOSTNAME,
            database    = MYSQL_DB
        )
        current_connection = conn
        return conn
    except mysql.connector.Error as err:
        error_and_exit(err)

def get_tables():
    global current_connection
    if current_connection is None:
        connect()

    try :
        cursor = current_connection.cursor()
        cursor.execute("SHOW TABLES")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        error_and_exit(err)

def close():
    global current_connection
    if current_connection is not None:
        current_connection.close()
        current_connection = None

def error_and_exit(err):
    cgiutils.print_error500(
            "An error occured connecting to the database!\n"+
            "Python MySQL Connector Error code: "+str(err.errno)
    )
    exit()