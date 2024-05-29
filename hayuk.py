import socket
import ssl

# Konfigurasi
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8080
REMOTE_HOST = 'example.com'
REMOTE_PORT = 443
DNS_SERVER = ('8.8.8.8', 53)  # Google DNS server
BUFFER_SIZE = 4096

# Fungsi untuk menangani koneksi TCP ke server jarak jauh
def handle_remote_client(client_socket):
    # Buat koneksi SSL ke server jarak jauh
    context = ssl.create_default_context()
    remote_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    remote_socket.connect((REMOTE_HOST, REMOTE_PORT))

    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        remote_socket.sendall(data)

        remote_data = remote_socket.recv(BUFFER_SIZE)
        if not remote_data:
            break
        client_socket.sendall(remote_data)

    remote_socket.close()
    client_socket.close()

# Fungsi untuk menangani permintaan DNS
def resolve_domain(domain):
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_socket.sendto(domain, DNS_SERVER)
    response, _ = dns_socket.recvfrom(1024)
    dns_socket.close()
    return response

# Fungsi utama
def main():
    # Buat socket untuk menerima koneksi dari klien lokal
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LOCAL_HOST, LOCAL_PORT))
    server_socket.listen(1)
    print(f'Menunggu koneksi di {LOCAL_HOST}:{LOCAL_PORT}...')
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Menerima koneksi dari {client_address[0]}:{client_address[1]}')

            # Baca alamat domain dari klien
            domain = client_socket.recv(BUFFER_SIZE)
            resolved_ip = resolve_domain(domain)
            print(f'Alamat IP yang diresolusi: {resolved_ip}')

            # Kirim ulang alamat IP ke klien
            client_socket.sendall(resolved_ip)

            # Tangani koneksi ke server jarak jauh
            handle_remote_client(client_socket)
    except KeyboardInterrupt:
        print("\nServer dihentikan.")

    server_socket.close()

if __name__ == "__main__":
    main()
