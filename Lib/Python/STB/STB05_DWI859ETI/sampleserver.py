import os
import http.server
import socketserver
import threading

def start_http_server():
        PORT = 8085  # Change port number if needed
        Handler = http.server.SimpleHTTPRequestHandler
        # Function to start the HTTP server
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"HTTP server running at http://192.168.1.101:{PORT}/")
            httpd.serve_forever()

# def access_html_file(self, html_file_path):
#     PORT = 8085  # Change port number if needed
#     # Handler = http.server.SimpleHTTPRequestHandler
#     # Function to access a specific HTML file
#     # Change directory to where the HTML file is located
#     os.chdir(os.path.dirname(os.path.abspath(html_file_path)))

#     # Extract the file name from the path
#     file_name = os.path.basename(html_file_path)
#     # Print the HTTP link to access the HTML file

#     http_link = f"http://192.168.1.101:{PORT}/home/ltts/Downloads/STB_Logs-2025-08-01 10_47_02.mp4"
#     print(f"Access your HTML file at: {http_link}")
#     return http_link

server_thread = threading.Thread(target=start_http_server)
server_thread.start()
