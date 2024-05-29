import socket
import dnslib
import http.server
import socketserver
import threading

# Reverse Proxy TCP
class TCPReverseProxy(threading.Thread):
    def __init__(self, src_port, dest_host, dest_port):
        super().__init__()
        self.src_port = src_port
        self.dest_host = dest_host
        self.dest_port = dest_port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as src_sock:
            src_sock.bind(('localhost', self.src_port))
            src_sock.listen()

            while True:
                conn, addr = src_sock.accept()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dest_sock:
                    dest_sock.connect((self.dest_host, self.dest_port))
                    threading.Thread(target=self.proxy, args=(conn, dest_sock)).start()

    def proxy(self, src_sock, dest_sock):
        while True:
            data = src_sock.recv(4096)
            if not data:
                break
            dest_sock.sendall(data)
        src_sock.close()
        dest_sock.close()

# Reverse Proxy DNS
class DNSProxy:
    def __init__(self, src_port, dest_host, dest_port):
        self.src_port = src_port
        self.dest_host = dest_host
        self.dest_port = dest_port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as src_sock:
            src_sock.bind(('localhost', self.src_port))
            while True:
                data, addr = src_sock.recvfrom(1024)
                request = dnslib.DNSRecord.parse(data)
                response = self.proxy(request)
                src_sock.sendto(response.pack(), addr)

    def proxy(self, request):
        # Implement DNS proxy logic here
        # Forward request to destination DNS server
        # Return response to client
        pass

# Reverse Proxy HTTP
class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        # Implement HTTP proxy logic here
        # Forward GET request to destination server
        # Return response to client

class HTTPProxy:
    def __init__(self, src_port):
        self.src_port = src_port

    def run(self):
        with socketserver.TCPServer(('localhost', self.src_port), HTTPHandler) as httpd:
            httpd.serve_forever()

# Example usage
if __name__ == "__main__":
    # Reverse Proxy TCP
    tcp_proxy = TCPReverseProxy(8080, 'destination_host', 80)
    tcp_proxy.start()

    # Reverse Proxy DNS
    dns_proxy = DNSProxy(53, 'destination_dns_server', 53)
    threading.Thread(target=dns_proxy.run).start()

    # Reverse Proxy HTTP
    http_proxy = HTTPProxy(8000)
    threading.Thread(target=http_proxy.run).start()
