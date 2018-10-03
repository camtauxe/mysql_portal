#!/usr/bin/python
import json
import cgi
import cgitb

from lib import cgiutils
from lib import sqlutils

cgitb.enable()

tables = list(map(lambda x: x[0], sqlutils.get_tables()))
json = json.dumps(tables)

cgiutils.print_response(json, "200 OK", "text/json")
