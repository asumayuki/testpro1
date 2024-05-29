from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

class ReverseProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "http://example.com" + self.path
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            content = response.read()
            self.send_response(response.code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(content)

def run(server_class=HTTPServer, handler_class=ReverseProxyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Reverse proxy berjalan di port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
