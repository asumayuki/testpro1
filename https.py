import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    while True:
        # Menerima data dari klien
        client_data = client_socket.recv(4096)
        if len(client_data) == 0:
            break
        
        # Memeriksa apakah permintaan adalah CONNECT
        if client_data.startswith(b"CONNECT"):
            # Merespons dengan 200 OK untuk permintaan CONNECT
            client_socket.send(b"HTTP/1.1 200 Connection established\r\n\r\n")
        else:
            # Mengirim data ke server backend
            remote_socket.send(client_data)
        
        # Menerima respons dari server backend
        remote_data = remote_socket.recv(4096)
        if len(remote_data) == 0:
            break
        
        # Mengirim respons kembali ke klien
        client_socket.send(remote_data)
    
    client_socket.close()
    remote_socket.close()

def run_reverse_proxy_server(local_host, local_port, remote_host, remote_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(5)
    print(f"Reverse proxy server berjalan di {local_host}:{local_port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Terhubung dari: {addr[0]}:{addr[1]}")
        
        # Memulai thread baru untuk menangani koneksi
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()

if __name__ == "__main__":
    local_host = "127.0.0.1"  # Ganti dengan alamat lokal yang diinginkan
    local_port = 8888  # Ganti dengan port lokal yang diinginkan
    remote_host = "backend_server_address"  # Ganti dengan alamat server backend
    remote_port = 443  # Ganti dengan port server backend HTTPS
    
    run_reverse_proxy_server(local_host, local_port, remote_host, remote_port)
