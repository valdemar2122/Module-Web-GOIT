from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
from datetime import datetime
import json
import socket
import threading


def save_to_json(data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    json_data = {
        current_time: {
            "username": data.get("username", ""),
            "message": data.get("message", ""),
        }
    }

    try:
        with open("storage/data.json", "r") as file:
            file_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        file_data = {}

    file_data.update(json_data)

    with open("storage/data.json", "w") as file:
        json.dump(file_data, file, indent=2)


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        save_to_json(data_dict)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


udp_running = True


def stop_udp_server():
    global udp_running
    udp_running = False


def udp_server():
    UDP_HOST = "127.0.0.1"
    UDP_PORT = 5000

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_HOST, UDP_PORT))

    while udp_running:
        data, addr = udp_socket.recvfrom(1024)
        data_str = data.decode()
        print(f"Received UDP data: {data_str}")
        # Process data or save to JSON file here
        # Example: You can call the save_to_json function passing the parsed data as a dictionary
        parsed_data = dict(item.split("=") for item in data_str.split("&"))
        save_to_json(parsed_data)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)

    try:
        http_thread = threading.Thread(target=http.serve_forever)
        udp_thread = threading.Thread(target=udp_server)

        http_thread.start()
        udp_thread.start()

        http_thread.join()
        udp_thread.join()

    except KeyboardInterrupt:
        http.server_close()
        print(" HTTP Server Closed")


if __name__ == "__main__":
    run()
