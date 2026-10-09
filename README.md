# COSC 350 - Simple HTTP Web Server

## Overview

This project implements a basic HTTP/1.1 web server in Python using the built-in `socket` library. It accepts client connections, processes HTTP requests, and returns responses based on the requested resource and HTTP method.

The server was developed for COSC 350 to demonstrate the fundamentals of network programming and the HTTP request-response protocol.

## Features

* **GET Requests:** Serves requested files from the server's web directory.
* **HEAD Requests:** Returns response headers without sending the response body.
* **Conditional GET:** Supports the `If-Modified-Since` header and returns `304 Not Modified` when the requested file has not changed.
* **HTTP Status Codes:** Handles `200 OK`, `304 Not Modified`, `403 Forbidden`, `404 Not Found`, and `501 Not Implemented`.
* **Response Headers:** Includes headers such as `Date`, `Server`, `Content-Length`, `Last-Modified`, and `Connection`.
* **Persistent Connections:** Processes multiple requests over the same client connection.
* **Path Protection:** Blocks requests that attempt to access files outside the server's root directory.
* **Request and Response Logging:** Prints received requests and response information to the console.

## Technologies

* Python 3
* Socket programming
* HTTP/1.1
* Git and GitHub

## Project Structure

```text
COSC350-WebServer/
├── server.py
├── www/
│   └── test.txt
└── README.md
```

`server.py` contains the web server implementation. The `www` directory contains the files that the server can serve to clients.

## Getting Started

### Prerequisites

* Python 3 installed on your computer
* A terminal or code editor, such as Visual Studio Code

### Installation

1. Clone the repository or download the project files.
2. Open the project directory in your terminal or VS Code.
3. Make sure the `www` directory exists and contains the files you want to serve.

### Running the Server

Run the following command from the project directory:

```bash
python3 server.py
```

The server listens on port `50000` and prints a message when it is ready to accept connections.

### Testing the Server

Open a web browser and visit:

```text
http://127.0.0.1:50000/test.txt
```

You can also test specific HTTP methods and headers using `curl`.

**GET request:**

```bash
curl -i http://127.0.0.1:50000/test.txt
```

**HEAD request:**

```bash
curl -I http://127.0.0.1:50000/test.txt
```

**Conditional GET request:**

```bash
curl -i -H "If-Modified-Since: Fri, 09 Oct 2026 19:14:17 GMT" http://127.0.0.1:50000/test.txt
```

The conditional request returns `304 Not Modified` if the file's modification time is no later than the specified date; otherwise, it returns the file with `200 OK`.

Press `Ctrl+C` in the terminal to stop the server.

## Learning Objectives

This project demonstrates practical experience with TCP sockets, HTTP request parsing, response construction, file handling, HTTP headers, conditional requests, persistent connections, and basic path security.

## Course

COSC 350 - Computer Networks / Network Programming

**Language:** Python
