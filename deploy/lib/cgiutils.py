import sys

# Contains functions for writing HTTP Responses
# to stdout

# Print a complete HTTP response to stdout with the
# given status, content type and response text.
# Text is encoded into UTF-8 and and the raw bytes
# are written stdout
def print_response(response_text, status, content_type):
    response = (
        "Status: "+status+"\n"+
        "Content-Type: "+content_type+";charset=\"UTF-8\"\n"+
        "\n"+
        response_text
    )
    if not response.endswith("\n"):
        response += "\n"
    sys.stdout.buffer.write(response.encode('utf-8'))

# Print a complete HTTP response giving a 400 (Bad Request)
# with the given message as the response text (as plaintext)
def print_error400(message):
    print_response(message, "400 Bad Request", "text/plain")

# Print a complete HTTP response giving a 403 (Forbidden)
# with the given message as the response text (as plaintext)
def print_error403(message):
    print_response(message, "403 Forbidden", "text/plain")

# Print a complete HTTP response giving a 404 (Not Found)
# with the given message as the response text (as plaintext)
def print_error404(message):
    print_response(message, "404 Not Found", "text/plain")

# Print a complete HTTP response giving a 405 (Method Not Allowed)
# with the given message as the response text (as plaintext)
def print_error405(message):
    print_response(message, "405 Method Not Allowed", "text/plain")

# Print a complete HTTP response giving a 500 (Internal Server Error)
# with the given message as the response text (as plaintext)
def print_error500(message):
    print_response(message, "500 Internal Server Error", "text/plain")
