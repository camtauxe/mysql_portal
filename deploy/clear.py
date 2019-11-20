#!/usr/bin/python3
import json
import cgi
import cgitb

from lib import cgiutils
from lib import sqlutils

# Clear all of the data from a given table

# Read the table to query from HTTP request parameters (in the URL)
params = cgi.FieldStorage()
table = params.getvalue('t')

# Return a 400 error if no table parameter was provided
if not table:
    cgiutils.print_error400("Invalid request parameters:\n"+
        "You must provide the table name as a parameter 't'")
    exit()

# Return a 400 error if the provided table does not exist
tables = sqlutils.get_tables()
if table not in tables:
    cgiutils.print_error400("The table '"+table+"' does not exist!")
    exit()

# Do deletion
sqlutils.clear_table(table)

# No need to close connection, because when performing volatile operations
# (i.e. changing the state of the database), the connection is closed
# immediately for security

# Print the HTTP response
cgiutils.print_response("OK", "200 OK", "text/plain")
