import socket
import threading

# Definisikan host dan port untuk proxy server
proxy_host = '0.0.0.0'  # Mengikuti semua alamat IP yang tersedia di mesin
proxy_port = 8888  # Port proxy server

# Definisikan host dan port untuk server asli (backend server)
server_host = 'example.com'  # Ganti dengan host backend server yang ingin Anda reverse proxy
server_port = 80  # Ganti dengan port backend server yang ingin Anda reverse proxy

def handle_client(client_socket):
    # Terhubungkan ke server asli (backend server)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_host, server_port))

    # Teruskan data dari client ke server
    while True:
        # Terima data dari client
        client_data = client_socket.recv(4096)
        if not client_data:
            break
        # Teruskan data dari client ke server
        server_socket.sendall(client_data)

        # Terima data dari server
        server_data = server_socket.recv(4096)
        if not server_data:
            break
        # Teruskan data dari server ke client
        client_socket.sendall(server_data)

    # Tutup koneksi ke client dan server
    client_socket.close()
    server_socket.close()

def main():
    # Buat socket untuk proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Ikuti semua alamat IP yang tersedia di mesin
    proxy_socket.bind((proxy_host, proxy_port))
    # Dengarkan koneksi masuk
    proxy_socket.listen(5)
    print(f"[*] Listening on {proxy_host}:{proxy_port}")

    while True:
        # Terima koneksi dari client
        client_socket, client_address = proxy_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        
        # Kelola setiap koneksi client dengan menggunakan thread terpisah
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
