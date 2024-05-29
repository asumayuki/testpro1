import socket
import ssl

# Konfigurasi
REMOTE_HOST = '8.8.8.8'  # DNS server yang akan dipanggil
REMOTE_PORT = 53  # Port DNS
PROXY_HOST = 'example.com'  # Host proxy yang akan di-forwardkan
PROXY_PORT = 443  # Port proxy yang akan di-forwardkan
LOCAL_PORT = 8053  # Port lokal untuk menerima koneksi

def handle_client(client_socket):
    # Membaca data dari klien
    data = client_socket.recv(4096)

    # Mendeteksi protokol HTTP
    if b'HTTP' in data:
        # Meneruskan permintaan HTTP ke server proxy
        remote_socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket_proxy = ssl.wrap_socket(remote_socket_proxy, ssl_version=ssl.PROTOCOL_TLS)
        remote_socket_proxy.connect((PROXY_HOST, PROXY_PORT))
        remote_socket_proxy.sendall(data)

        # Menerima respons dari server proxy dan meneruskannya ke klien
        while True:
            response = remote_socket_proxy.recv(4096)
            if not response:
                break
            client_socket.sendall(response)

        remote_socket_proxy.close()
    else:
        # Meneruskan permintaan DNS ke server DNS melalui koneksi TLS
        remote_socket_dns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket_dns = ssl.wrap_socket(remote_socket_dns, ssl_version=ssl.PROTOCOL_TLS)
        remote_socket_dns.connect((REMOTE_HOST, REMOTE_PORT))
        remote_socket_dns.sendall(data)

        # Menerima respons dari server DNS dan meneruskannya ke klien
        response = remote_socket_dns.recv(4096)
        client_socket.sendall(response)

        remote_socket_dns.close()

    # Menutup koneksi dengan klien
    client_socket.close()

def main():
    # Membuat socket untuk menerima koneksi dari klien
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind(('localhost', LOCAL_PORT))
    local_socket.listen(5)

    print(f'Menyimak koneksi di port {LOCAL_PORT}...')

    while True:
        # Menerima koneksi dari klien
        client_socket, addr = local_socket.accept()
        print(f'Menerima koneksi dari {addr[0]}:{addr[1]}')

        # Menangani koneksi dari klien
        handle_client(client_socket)

if __name__ == "__main__":
    main()
