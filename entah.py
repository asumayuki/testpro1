import socket
import ssl

# Konfigurasi
LISTEN_HOST = '0.0.0.0'  # Host yang mendengarkan koneksi masuk
LISTEN_PORT = 8000       # Port untuk mendengarkan koneksi masuk
DESTINATION_HOST = 'example.com'  # Host tujuan
DESTINATION_PORT = 443   # Port tujuan

def handle_client(client_socket):
    # Buat koneksi ke tujuan
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((DESTINATION_HOST, DESTINATION_PORT))
    
    # Baca data dari klien dan kirimkan ke tujuan
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        destination_socket.send(data)
        
        # Terima balasan dari tujuan dan kirimkan ke klien
        reply = destination_socket.recv(4096)
        client_socket.send(reply)
    
    # Tutup koneksi
    client_socket.close()
    destination_socket.close()

# Buat socket untuk mendengarkan koneksi masuk
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((LISTEN_HOST, LISTEN_PORT))
server_socket.listen(5)

print(f"Menunggu koneksi masuk di {LISTEN_HOST}:{LISTEN_PORT}...")

while True:
    client_socket, _ = server_socket.accept()
    print("Koneksi masuk diterima!")
    
    # Mulai penanganan klien dalam thread terpisah
    handle_client(client_socket)
