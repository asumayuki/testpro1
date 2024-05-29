import socket
import threading
import ssl

class TCPProxyServer:
    def __init__(self, local_host, local_port, dns_host, http_host, http_port):
        self.local_host = local_host
        self.local_port = local_port
        self.dns_host = dns_host
        self.http_host = http_host
        self.http_port = http_port

    def handle_client(self, client_socket):
        # Baca data dari klien
        data = client_socket.recv(4096)

        # Teruskan data ke server DNS
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dns_socket.connect((self.dns_host, 53))
        dns_socket.sendall(data)
        dns_response = dns_socket.recv(4096)
        dns_socket.close()

        # Ambil IP dari respons DNS
        ip_address = self.get_ip_from_dns_response(dns_response)

        # Teruskan data ke server HTTP
        http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_socket.connect((ip_address, self.http_port))
        http_socket.sendall(data)

        # Baca dan teruskan respons dari server HTTP ke klien
        while True:
            response_data = http_socket.recv(4096)
            if len(response_data) > 0:
                client_socket.send(response_data)
            else:
                break

        # Tutup koneksi
        http_socket.close()
        client_socket.close()

    def get_ip_from_dns_response(self, response):
        # Logika untuk mengekstrak alamat IP dari respons DNS
        pass

    def start(self):
        # Buat socket TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.local_host, self.local_port))
        server_socket.listen(5)
        print(f"[*] Listening on {self.local_host}:{self.local_port}")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("[*] Exiting.")

if __name__ == "__main__":
    local_host = "127.0.0.1"
    local_port = 8080
    dns_host = "8.8.8.8"  # DNS server
    http_host = "example.com"  # HTTP server
    http_port = 80

    proxy_server = TCPProxyServer(local_host, local_port, dns_host, http_host, http_port)
    proxy_server.start()
