#!/usr/bin/python3
import json
import cgi
import cgitb

from lib import cgiutils
from lib import sqlutils

# Return all of the data in the table specified in the 't' HTTP request
# parameter in a JSON format. All data is converted to strings

# Enabling cgitb will cause a web page to be sent back containing error
# information in the event an uncaught error occurs. This is useful for
# debugging, but we don't want to expose details about our code to people
# visiting the site, so comment it out once you know things are working.
# With it disabled, an uncaught error will cause the web server to return
# a standard 500 Internal Server Error
#cgitb.enable()

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

# Query for all data and parse into JSON
results = sqlutils.exec_readonly_query("SELECT * FROM "+table)
results_json = json.dumps(results)

# Using the database established a connection
# Since we're done with it, we close the connection
sqlutils.close()

# Print the HTTP response
cgiutils.print_response(results_json, "200 OK", "text/json")
