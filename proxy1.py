import socket
import threading

# Fungsi untuk menangani koneksi dari client ke server tujuan
def handle_client(client_socket, remote_host, remote_port):
    # Membuat koneksi ke server tujuan
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    # Meneruskan data dari client ke server tujuan
    while True:
        # Menerima data dari client
        client_data = client_socket.recv(4096)
        if not client_data:
            break
        # Mengirim data dari client ke server tujuan
        remote_socket.sendall(client_data)
        
        # Menerima data dari server tujuan
        remote_data = remote_socket.recv(4096)
        if not remote_data:
            break
        # Mengirim data dari server tujuan ke client
        client_socket.sendall(remote_data)
    
    # Menutup koneksi
    client_socket.close()
    remote_socket.close()

# Fungsi utama untuk menjalankan reverse proxy
def main():
    # Konfigurasi host dan port untuk proxy
    local_host = '127.0.0.1'
    local_port = 8888
    
    # Konfigurasi host dan port untuk server tujuan
    remote_host = 'remote_server_ip_address'
    remote_port = 80
    
    # Membuat socket untuk menerima koneksi dari client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_host, local_port))
    server_socket.listen(5)
    print("[*] Listening on {}:{}".format(local_host, local_port))
    
    while True:
        # Menerima koneksi dari client
        client_socket, addr = server_socket.accept()
        print("[*] Accepted connection from {}:{}".format(addr[0], addr[1]))
        
        # Membuat thread untuk menangani koneksi dari client ke server tujuan
        proxy_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()

if __name__ == "__main__":
    main()
