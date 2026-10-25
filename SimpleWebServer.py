import socket

# 1. LAYER 4 (TRANSPORT): Set up the TCP Pipe
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# REUSEADDR allows you to restart the server immediately without waiting for the OS to release the port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5) # Increased backlog to queue up to 5 incoming connections

print("Server is running continuously. Open http://127.0.0.1:8080 in your browser...")
print("Press Ctrl+C in the terminal to stop the server.\n")

try:
    while True:
        # Wait for a browser to connect via TCP
        client_socket, client_address = server_socket.accept()
        print(f"Connection accepted from {client_address}")
        
        try:
            # 2. LAYER 7 (APPLICATION): Read the raw data coming down the pipe
            raw_request = client_socket.recv(1024)
            if not raw_request:
                continue # If the browser connected but sent no data, skip to next loop
                
            http_request_text = raw_request.decode('utf-8', errors='ignore')
            
            print("\n--- RAW HTTP REQUEST RECEIVED ---")
            # Print just the first line of the request to keep terminal clean, or print all
            print(http_request_text if http_request_text else "")
            print("---------------------------------\n")
            
            # 3. LAYER 7 (APPLICATION): Formulate a valid HTTP Response
            html_body = "<html><body><h1>Hello from Layer 7! It keeps working!</h1></body></html>"
            body_bytes = html_body.encode('utf-8')
            
            status_line = "HTTP/1.1 200 OK\r\n"
            headers = f"Content-Type: text/html\r\nContent-Length: {len(body_bytes)}\r\n\r\n"
            
            # Combine everything into raw bytes
            full_http_response = status_line.encode('utf-8') + headers.encode('utf-8') + body_bytes
            print(full_http_response)
            # 4. LAYER 4 / LAYER 1: Push the HTTP data back down the TCP pipe
            client_socket.sendall(full_http_response)
            
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            # Crucial: Always close the client socket so the browser knows we are done sending data
            client_socket.close()

except KeyboardInterrupt:
    print("\nServer shutting down gracefully.")
finally:
    server_socket.close()
