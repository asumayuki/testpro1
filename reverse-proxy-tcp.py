import socket
import threading

# Fungsi untuk menangani koneksi dari client ke server tujuan
def handle_client(client_socket, target_host, target_port):
    # Terima data dari client
    request = client_socket.recv(4096)
    
    # Teruskan data ke server tujuan
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((target_host, target_port))
        server_socket.sendall(request)
        
        # Terima balasan dari server
        response = server_socket.recv(4096)
        
        # Teruskan balasan ke client
        client_socket.sendall(response)

# Fungsi untuk membuat proxy TCP
def proxy_server(bind_host, bind_port, target_host, target_port):
    # Buat socket untuk menerima koneksi dari client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.bind((bind_host, bind_port))
        proxy_socket.listen(5)
        print(f"[*] Listening on {bind_host}:{bind_port}")
        
        while True:
            client_socket, _ = proxy_socket.accept()
            print(f"[*] Accepted connection from {client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}")
            
            # Mulai thread baru untuk menangani koneksi dari client ke server tujuan
            proxy_thread = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
            proxy_thread.start()

# Menentukan konfigurasi proxy
bind_host = '0.0.0.0'
bind_port = 8888
target_host = '127.0.0.1'  # Ganti dengan alamat IP server tujuan
target_port = 8080  # Ganti dengan port server tujuan

# Jalankan reverse proxy
proxy_server(bind_host, bind_port, target_host, target_port)
