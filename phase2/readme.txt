To deploy the website to the server, run the shell script like so:

    sh deploySite.sh

Note that everything within the deploy directory will be sent to the server,
so be careful about including any sensitive information within that directory.

Anything within the 'deploy/private' and 'deploy/lib' directory will not be
accessible as the web server is configured to deny access to these directories

The web server is configured to interpret any request for a python file (.py)
within the deploy directory as a CGI (Common Gateway Interface) script.
This means that the web server will run the script and return whatever that
script sends to standard output as the HTTP response.