#!/usr/bin/python3
import json
import cgi
import cgitb

from lib import cgiutils
from lib import sqlutils

# Respond with a list (in JSON format) of the names of all of
# the tables in the database

# Enabling cgitb will cause a web page to be sent back containing error
# information in the event an uncaught error occurs. This is useful for
# debugging, but we don't want to expose details about our code to people
# visiting the site, so comment it out once you know things are working.
# With it disabled, an uncaught error will cause the web server to return
# a standard 500 Internal Server Error
#cgitb.enable()

# Get the list of tables and convert to a JSON string
tables = sqlutils.get_tables()
tables_json = json.dumps(tables)

# Calling get_tables() established a database connection.
# Since we're done with it, we close the connection
sqlutils.close()

# Print the HTTP response
cgiutils.print_response(tables_json, "200 OK", "text/json")
