The 'deploy' directory contains all of the files that are sent to the remote
server (mysql.camerontauxe.com). The Web Server is configured so that when
requesting any python file, instead of returning the file, the script is
executed via CGI to generate the web page. The server is also configured to
deny any requests to the contents of the 'private' and 'lib' directories.'
The contents of 'lib' are used by the python scripts and contain common
functions for interacting with MySQL or using CGI. The 'private' directory is
for anything else that needs to be on the server but cannot be publicly
accessible to the internet (currently unused).

The 'data' directory contains the script for generating random sets of data.

The 'doc' directory contains the lab writeup