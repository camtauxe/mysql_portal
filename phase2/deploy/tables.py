#!/usr/bin/python
import json
import cgi
import cgitb

from lib import cgiutils
from lib import sqlutils

# Respond with a list (in JSON format) of the names of all of
# the tables in the database

# Get the list of tables and convert to a JSON string
tables = sqlutils.get_tables()
json = json.dumps(tables)

# Calling get_tables() established a database connection.
# Since we're done with it, we close the connection
sqlutils.close()

# Print the HTTP response
cgiutils.print_response(json, "200 OK", "text/json")
