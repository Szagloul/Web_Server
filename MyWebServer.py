# Skeleton program
import socket
import sys
import os
from email.utils import formatdate, parsedate_to_datetime

HOST = None                                     # Symbolic name meaning all available interfaces
PORT = 50000                                    # Arbitrary non-privileged port
SERVER_ROOT = os.path.abspath("www")            # Root directory for the web server files

s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(sa)
        s.listen(1)
        print('Server is running. Waiting for connection...')
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept()
    try:
        with conn:
            print('Connected by', addr)
            while True:
                http_request = conn.recv(1024).decode('utf-8', errors='ignore')
                if not http_request: break

                print("===== Raw HTTP Request ====")
                print(http_request)

                request_line = http_request.splitlines()[0]
                parts = request_line.split()
                request_headers = {}
                for line in http_request.splitlines()[1:]:
                    if ":" in line:
                        header_name, header_value = line.split(":", 1)
                        request_headers[header_name.strip().lower()] = header_value.strip()
                if_modified_since = request_headers.get("if-modified-since")
                if_modified_since_date = None
                if if_modified_since:
                    try:
                        if_modified_since_date = parsedate_to_datetime(if_modified_since)
                    except (TypeError, ValueError):
                        if_modified_since_date = None

                request_method = parts[0]
                request_path = parts[1]
                request_version = parts[2]

                print("Request Method:", request_method)
                print("Request Path:", request_path)
                print("Request Version:", request_version)  

                if request_method not in ("GET", "HEAD"):
                    status_line = "501 Not Implemented"
                    response_body = b"501 Not Implemented"
                else:
                    if request_path == "/":         
                        request_path = "/index.html"

                    file_path = os.path.join(SERVER_ROOT, request_path.lstrip("/")) # Joins the Root with the requestedpath
                    file_path = os.path.abspath(file_path)                          # Convert to an absolute path

                    print("File Path:", file_path)

                    if "../" in request_path or "..\\" in request_path:
                        status_line = "403 Forbidden"                   # Sets the status line for special forbidden cases
                        response_body = b"403 Forbidden"                # Sets the response body for special forbidden cases
                    elif not file_path.startswith(SERVER_ROOT + os.sep) and file_path != SERVER_ROOT:
                        status_line = "403 Forbidden"                   # Sets the status line for a forbidden response
                        response_body = b"403 Forbidden"                # Sets the response body for a forbidden response   
                    elif os.path.exists(file_path) and os.path.isfile(file_path):
                        status_line = "200 OK"                          # Sets the status line for a successful response
                        with open(file_path, "rb") as file:             # Opens requested file in binary mode
                            response_body = file.read()                 # Reads the entire content of the requested file into response_body
                        last_modified = formatdate(os.path.getmtime(file_path), usegmt=True)
                        if if_modified_since_date and request_method == "GET":
                            file_mtime = os.path.getmtime(file_path)
                            if int(file_mtime)<= int(if_modified_since_date.timestamp()):
                                status_line = "304 Not Modified"        # Sets the status line for a not modified response
                                response_body = b""                     # Sets the response body for a not modified response
                    else:
                        status_line = "404 Not Found"                   # Sets the status line for a not found response
                        response_body = b"404 Not Found"                # Sets the response body for a not found response
                
                content_length = len(response_body)
                
                response_headers = (
                    f"HTTP/1.1 {status_line}\r\n"                                               # Include the HTTP status line in the response headers
                    "Server: COSC350-WebServer\r\n"                                             # Include the server header in the response
                    "Content-Type: text/html; charset=utf-8\r\n"                                # Include the content type header in the response
                    "Connection: keep-alive\r\n"                                                     # Include the connection header in the response
                    f"Date: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\n"       # Include the date header in the response
                )
                if status_line != "304 Not Modified":
                    response_headers += f"Content-Length: {content_length}\r\n"                 # 304 not modified omits content length header

                if status_line == "200 OK":
                    response_headers += f"Last-Modified: {last_modified}\r\n"                   # 200 OK includes last modified header
                
                response_headers += "\r\n"

                if request_method == "HEAD":
                    conn.sendall(response_headers.encode("utf-8"))                      # Sends only the HTTP response headers for a HEAD request
                else:
                    conn.sendall(response_headers.encode("utf-8") + response_body)      # Sends the complete HTTP response to client 
                
                print("===== HTTP Response Sent =====")     # Indicates that the HTTP response has been sent to the client
                print(response_headers)                     # Prints the HTTP response headers
                print(response_body.decode("utf-8", errors="replace"))        # Prints the HTTP response body

                

    except Exception as e:
        print("Error:", e)