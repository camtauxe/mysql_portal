import mysql.connector
import csv
from io import StringIO

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
MYSQL_DB        = 'cs482team'

MYSQL_READONLY_USER      = 'readonly'
MYSQL_READONLY_PASSWORD  = None

MYSQL_VOLATILE_USER      = 'webserver'
MYSQL_VOLATILE_PASSWORD  = 'C$482pass'

READONLY_MODE = 0
VOLATILE_MODE = 1

MAX_ROWS = 100

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
# and get all of the results. The data is formatted using the
# serialize_cursor() function, show see the documentation for
# that to understand the format of the data.
# 
# Instances of '%s' in sql_string will be safely replaced by
# corresponding values in values_tuple. Do this whenever possible to
# prevent SQL injection.
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
        dicts = serialize_cursor(cursor)
        cursor.close()
        return dicts
    except mysql.connector.Error as err:
        error_and_exit(err)

# Serialize the results stored in a cursor into a dictionary for easy
# conversion to JSON later.
#
# The dictionary has three fields: 'columns', 'rows' and 'data'
# 'columns' is a list of strings giving the names of each of the columns
# in the data.
# 'rows' is the total number of rows in the results.
# 'data' is a list of lists representing the data.
# The order of the data within a row matches the order the of 
# the columns in the 'columns' list.
#
# The data is truncated according to the value of MAX_ROWS, so even if the
# cursor returned more rows, they are not included in the serialization.
# But the 'rows' value will still refer to the total number of rows.
# Note that all data is converted to strings during this process
def serialize_cursor(cursor):
    col_names = [d[0].lower() for d in cursor.description]

    serialized = {'columns': col_names, 'data': []}
    # Fetch MAX_ROWS results and add them to the data list
    rows = cursor.fetchmany(MAX_ROWS)
    for row in rows:
        as_strings = [str(d) for d in row]
        serialized['data'].append(as_strings)
    # Fetch and discard the remaining results to get the row count
    # We fetch rows 1000 at a time to avoid filling up our memory
    more_rows = cursor.fetchmany(1000)
    while more_rows != []:
        more_rows = cursor.fetchmany(1000)
    serialized['rows'] = cursor.rowcount
    return serialized

# Insert the given data (as a CSV string) into the given table
# using the given mode ('single' or 'bulk').
#
# Before attempting to insert, the data currently in the table is cleared.
# If a connection has not already been established, or if one is
# established but in read-only mode, the connection will be re-established
# in volatile mode. For security, because this uses volatile mode, the 
# connection will be closed immediately afterwards.
def insert_data(table, mode, data):
    clear_table(table)
    global current_connection, current_mode
    if current_mode is not VOLATILE_MODE:
        connect_volatile()
    try:
        cursor = current_connection.cursor()
        # Get the number of columns in the table
        cursor.execute("SHOW columns FROM "+table)
        num_columns = len([col[0] for col in cursor.fetchall()])

        # Create an insert statement using '%s' for each value we insert
        insert_stmt = "INSERT INTO "+table+" VALUES ("+("%s, "*(num_columns-1))+"%s)"

        # Parse data string as a CSV file
        dataIO = StringIO(data)
        reader = csv.reader(dataIO)
        for row in reader:
            # Error if any row has an incorrect number of values
            if len(row) is not num_columns:
                cgiutils.print_error400("Error parsing data!\nIncorrect number of values in a row!")
                exit()
            # Insert data
            cursor.execute(insert_stmt, tuple(row))
            # If in 'single' mode, commit after every insertion
            if mode == 'single':
                current_connection.commit()

        # If in 'bulk' mode, we need to commit only at the end
        if mode == 'bulk':
            current_connection.commit()
        cursor.close()
        current_connection.close()
    except mysql.connector.Error as err:
        error_and_exit(err)

# Delete all of the data from the given table.
# Note that this does not drop the table from the schema,
# rahter it deletes every row in the table.
#
# If a connection has not already been established, or if one is
# established but in read-only mode, the connection will be re-established
# in volatile mode. For security, because this uses volatile mode, the 
# connection will be closed immediately afterwards.
def clear_table(table):
    global current_connection, current_mode
    if current_mode is not VOLATILE_MODE:
        connect_volatile()
    try:
        cursor = current_connection.cursor()
        cursor.execute("DELETE FROM "+table)
        current_connection.commit()
        close()
    except mysql.connector.Error as err:
        error_and_exit(err)

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

