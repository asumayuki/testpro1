import socket
import ssl
import threading

# Fungsi untuk menangani koneksi HTTP
def handle_http(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        # Baca data dari client
        client_data = client_socket.recv(4096)
        if not client_data:
            break

        # Teruskan data ke server HTTPS
        remote_socket.sendall(client_data)

        # Terima balasan dari server HTTPS
        remote_data = remote_socket.recv(4096)
        if not remote_data:
            break

        # Teruskan balasan ke client
        client_socket.sendall(remote_data)

    client_socket.close()
    remote_socket.close()

# Fungsi untuk menangani koneksi DNS
def handle_dns(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # Baca data dari client
        client_data, client_addr = client_socket.recvfrom(4096)
        if not client_data:
            break

        # Teruskan data ke server DNS
        remote_socket.sendto(client_data, (remote_host, remote_port))

        # Terima balasan dari server DNS
        remote_data, remote_addr = remote_socket.recvfrom(4096)
        if not remote_data:
            break

        # Teruskan balasan ke client
        client_socket.sendto(remote_data, client_addr)

    client_socket.close()
    remote_socket.close()

def main():
    local_host = '127.0.0.1'
    http_local_port = 8888
    dns_local_port = 53
    remote_host = 'destination_host'
    https_remote_port = 443
    dns_remote_port = 53

    # Menggunakan thread untuk menangani koneksi HTTP
    http_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server_socket.bind((local_host, http_local_port))
    http_server_socket.listen(5)
    print(f'[*] Listening for HTTP connections on {local_host}:{http_local_port}')
    http_thread = threading.Thread(target=handle_http, args=(http_server_socket, remote_host, https_remote_port))
    http_thread.start()

    # Menggunakan thread untuk menangani koneksi DNS
    dns_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_server_socket.bind((local_host, dns_local_port))
    print(f'[*] Listening for DNS requests on {local_host}:{dns_local_port}')
    dns_thread = threading.Thread(target=handle_dns, args=(dns_server_socket, remote_host, dns_remote_port))
    dns_thread.start()

if __name__ == '__main__':
    main()
  
