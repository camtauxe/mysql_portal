#!/usr/bin/python3
import json
import cgi
import cgitb
from time import time

from lib import cgiutils
from lib import sqlutils

# Return all of the data in the table specified in the 't' HTTP request
# parameter in a JSON format. All data is converted to strings

# Read the table to query from HTTP request parameters (in the URL)
params = cgi.FieldStorage()
query = params.getvalue('q')

# Return a 400 error if no query parameter was provided
if not query:
    cgiutils.print_error400("Invalid request parameters:\n"+
        "You must provide the query as a parameter 'q'")
    exit()

# Execute query and calculate time
before = time() 
results = sqlutils.exec_readonly_query(query)
after = time()

# Add time to results then convert to json
results['time'] = str("%.3f" % (after - before))
results_json = json.dumps(results)

# Using the database established a connection
# Since we're done with it, we close the connection
sqlutils.close()

# Print the HTTP response
cgiutils.print_response(results_json, "200 OK", "text/json")
