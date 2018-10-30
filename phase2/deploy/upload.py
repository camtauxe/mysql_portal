#!/usr/bin/python3
import json
import sys
import cgi
from time import time

from lib import cgiutils
from lib import sqlutils

# Take an uploaded csv file and insert it into a table in the manner
# corresponding to the specified type 'single' or 'bulk.' If successful,
# return a json specifiying the time it took for the operation to complete.

# Read data from stdin
data = sys.stdin.read()

# Read the form data parameters
params = cgi.FieldStorage()
insertType = params.getvalue('type') # either 'bulk' or 'single'
table = params.getvalue('t')

# Return a 400 error if no table parameter was provided
if not table:
    cgiutils.print_error400("Invalid request parameters:\n"+
        "You must provide a table as a parameter 't'")
    exit()
# Return a 400 error if no type parameter was provided
if not insertType:
    cgiutils.print_error400("Invalid request parameters:\n"+
        "You must provide an insertion type as a parameter 'type'")
    exit()

# Return a 400 error if the provided insertion type is invalid
if insertType not in ['bulk','single']:
    cgiutils.print_error400("Invalid insertion type! Must be 'single' or 'bulk'")
    exit()

# Return a 400 error if the provided table does not exist
tables = sqlutils.get_tables()
if table not in tables:
    cgiutils.print_error400("The table '"+table+"' does not exist!")
    exit()

# Do insertion and calculate time
before = time()
sqlutils.insert_data(table,insertType,data)
after = time()
totalTime = str("%.3f" % (after - before))

# Print the HTTP response with a JSON string specifying the time
cgiutils.print_response("{\"time\": \""+totalTime+"\"}", "200 OK", "text/json")
