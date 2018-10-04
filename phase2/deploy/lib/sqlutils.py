import mysql.connector

from . import cgiutils

# Contains functions for interacting with
# the MySQL Database
# Maintains a current connection as a global variable.
# The connection can be established by calling connect()
# and closed by calling close().
# Most functions will automatically establish the connection
# first if they are called before the connection is established

# Constants
MYSQL_HOSTNAME  = 'localhost'
MYSQL_DB        = 'cs482'

MYSQL_READONLY_USER      = 'readonly'
MYSQL_READONLY_PASSWORD  = None

MYSQL_VOLATILE_USER      = 'webserver'
MYSQL_VOLATILE_PASSWORD  = 'C$482pass'

READONLY_MODE = 0
VOLATILE_MODE = 1

# Global variables
current_connection  = None
current_mode        = None

# Connect to the database as a "read-only" user
# and return the connection object
# If an error occurs, a 500 HTTP response will be printed
# and the script will immediately exit
#
# If there is already a current connection, that connection will
# be closed and replaced with this one
def connect_readonly():
    global current_connection, current_mode
    close()
    try:
        conn = mysql.connector.connect(
            user        = MYSQL_READONLY_USER,
            password    = MYSQL_READONLY_PASSWORD,
            host        = MYSQL_HOSTNAME,
            database    = MYSQL_DB
        )
        current_connection = conn
        current_mode = READONLY_MODE
        return conn
    except mysql.connector.Error as err:
        error_and_exit(err)

# Connect to the database as a "volatile" user with
# select, insert, update and delete permissions on the database
# and return the connection object
# If an error occurs, a 500 HTTP response will be printed
# and the script will immediately exit
#
# If there is already a current connection, that connection will
# be closed and replaced with this one
def connect_volatile():
    global current_connection, current_mode
    close()
    try:
        conn = mysql.connector.connect(
            user        = MYSQL_VOLATILE_USER,
            password    = MYSQL_VOLATILE_PASSWORD,
            host        = MYSQL_HOSTNAME,
            database    = MYSQL_DB
        )
        current_connection = conn
        current_mode = VOLATILE_MODE
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
        connect_readonly()
    try :
        cursor = current_connection.cursor()
        cursor.execute("SHOW TABLES")
        tuples = cursor.fetchall()
        cursor.close()
        return [t[0] for t in tuples]
    except mysql.connector.Error as err:
        error_and_exit(err)

# Execute a given query as the "read only" user on the database
# and get all of the results as a list of dictionaries
# 
# Instances of '%s' in sql_string will be safely replaced by
# corresponding values in values_tuple. Do this whenever possible to
# prevent SQL injection.
#
# Note that the returned data will all be represented as strings
# 
# If a connection has not already been established, or if one is
# established but in volatile mode, the connection will be re-established
# in read-only mode before the query is executed.
def exec_readonly_query(sql_string, values_tuple = ()):
    global current_connection, current_mode
    if current_mode is not READONLY_MODE:
        connect_readonly()
    try:
        cursor = current_connection.cursor()
        cursor.execute(sql_string, values_tuple)
        dicts = dicts_from_cursor(cursor)
        cursor.close()
        return dicts
    except mysql.connector.Error as err:
        error_and_exit(err)

# Get a list of dictionaries representing all of the results stored
# stored in the given cursor.
# All of the data will be represented as strings when returned
def dicts_from_cursor(cursor):
    col_names   = [d[0].lower() for d in cursor.description]
    rows        = cursor.fetchall()
    dicts       = []
    for row in rows:
        as_strings = [str(d) for d in row]
        dicts.append(dict(zip(col_names, as_strings)))
    return dicts

# Close the current connection
# If there is no current connection, this does nothing
def close():
    global current_connection, current_mode
    if current_connection is not None:
        current_connection.close()
        current_connection = None
        current_mode = None

# Print a 500 HTTP Response to stdout
# and immediately exit
def error_and_exit(err):
    cgiutils.print_error500(
            "A MySQL Error occurred!\n"+
            "Python MySQL Connector Error code: "+str(err.errno)+"\n"+
            str(err.msg)
    )
    exit()