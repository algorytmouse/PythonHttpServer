import socket
import os

def main():
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 8080

    # Define the folder containing the website resources
    CONTENT_DIR = "Content"

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Listening on port {SERVER_PORT} ...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1500).decode()
        if not request:
            client_socket.close()
            continue

        # Parse the HTTP request
        headers = request.split("\n")
        first_header_components = headers[0].split()

        http_method = first_header_components[0]
        path = first_header_components[1]

        # Default to index.html if the path is "/"
        if path == "/":
            path = "/index.html"

        # Construct the full file path
        file_path = os.path.join(CONTENT_DIR, path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            # File exists, read the content
            with open(file_path, "rb") as file:
                content = file.read()

            # Build the HTTP response
            response_headers = f"HTTP/1.1 200 OK\n\n"
            response = response_headers.encode() + content
        else:
            # File not found, send a 404 response
            response = b"HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>"

        # Send the response
        client_socket.sendall(response)
        client_socket.close()


if __name__ == "__main__":
    main()
