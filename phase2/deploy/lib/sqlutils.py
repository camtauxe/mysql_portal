import  mysql.connector

from .config import *
import cgiutils

# Contains functions for interacting with
# the MySQL Database
# Maintains a current connection as a global variable.
# The connection can be established by calling connect()
# and closed by calling close().
# Most functions will automatically establish the connection
# first if they are called before the connection is established

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

# Get a list of the names of all of the tables in the database
# If an error occurs, a 500 HTTP response will be printed
# and the script will immediately exit
#
# If there is no current connection, it will be established
def get_tables():
    global current_connection
    if current_connection is None:
        connect()

    try :
        cursor = current_connection.cursor()
        cursor.execute("SHOW TABLES")
        tuples = cursor.fetchall()
        return list(map(lambda x: x[0], tuples))
    except mysql.connector.Error as err:
        error_and_exit(err)

# Close the current connection
# If there is no current connection, this does nothing
def close():
    global current_connection
    if current_connection is not None:
        current_connection.close()
        current_connection = None

# Print a 500 HTTP Response to stdout
# and immediately exit
def error_and_exit(err):
    cgiutils.print_error500(
            "An error occured connecting to the database!\n"+
            "Python MySQL Connector Error code: "+str(err.errno)
    )
    exit()