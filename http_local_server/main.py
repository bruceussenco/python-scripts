import socket
import http.server
import socketserver

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)

print("Your computer name is: " + hostname)
print("Your computer IP address is: " + ip_addr)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
