import socket
import ssl
import threading

# Fungsi untuk menangani koneksi TCP ke TLS
def handle_tcp_to_tls(client_socket):
    # Terhubung ke server TLS
    server_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server_socket.connect(('tujuan_server', 443))  # Ganti 'tujuan_server' dengan alamat server yang diinginkan

    # Teruskan lalu lintas antara client dan server
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        server_socket.sendall(data)

    server_socket.close()
    client_socket.close()

# Fungsi untuk menangani koneksi HTTP
def handle_http(client_socket, client_addr):
    # Terhubung ke server HTTP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('tujuan_server', 80))  # Ganti 'tujuan_server' dengan alamat server yang diinginkan

    # Teruskan lalu lintas antara client dan server
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        server_socket.sendall(data)

    server_socket.close()
    client_socket.close()

# Fungsi untuk menangani koneksi DNS
def handle_dns(client_socket, client_addr):
    # Terhubung ke server DNS
    dns_server = ('8.8.8.8', 53)  # Ganti dengan server DNS yang diinginkan

    # Teruskan lalu lintas DNS antara client dan server
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns_sock:
            dns_sock.sendto(data, dns_server)
            dns_response, _ = dns_sock.recvfrom(4096)
            client_socket.sendall(dns_response)

    client_socket.close()

# Fungsi untuk memulai proxy TCP
def start_proxy_tcp(port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', port))
    proxy_socket.listen(5)

    while True:
        client_socket, client_addr = proxy_socket.accept()
        # Membaca pesan pertama dari client untuk menentukan protokol yang digunakan
        first_byte = client_socket.recv(1)
        client_socket.setblocking(True)  # Set socket ke mode blocking untuk menerima pesan secara utuh

        if first_byte == b'\x16':  # Jika pesan pertama adalah byte TLS (0x16)
            threading.Thread(target=handle_tcp_to_tls, args=(client_socket,)).start()
        elif first_byte == b'G':  # Jika pesan pertama adalah byte 'G' (representasi huruf pertama dari GET)
            threading.Thread(target=handle_http, args=(client_socket, client_addr)).start()
        else:  # Jika tidak sesuai dengan protokol yang dikenali, asumsikan protokol DNS
            threading.Thread(target=handle_dns, args=(client_socket, client_addr)).start()

# Jalankan proxy TCP pada port tertentu
start_proxy_tcp(8888)  # Ganti dengan port yang diinginkan
