import socket
import threading
import requests

# Fungsi untuk menangani koneksi TCP dari klien
def handle_client(client_socket, target_host, target_port):
    # Menghubungkan ke server target
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    # Meneruskan data dari klien ke server target
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        target_socket.send(data)

    # Menerima respons dari server target dan meneruskannya ke klien
    while True:
        response = target_socket.recv(4096)
        if not response:
            break
        client_socket.send(response)

    # Menutup koneksi
    client_socket.close()
    target_socket.close()

# Fungsi untuk menangani koneksi HTTP dari klien
def handle_http_client(client_connection, client_address):
    # Menerima request HTTP dari klien
    request_data = client_connection.recv(1024)

    # Mengirimkan request HTTP ke server target
    response = requests.get(request_data)

    # Mengirimkan respons dari server target kembali ke klien
    client_connection.sendall(response.content)

    # Menutup koneksi
    client_connection.close()

def main():
    # Konfigurasi proxy server
    proxy_host = '127.0.0.1'
    proxy_port = 8888

    # Server target
    target_host = 'example.com'
    target_port = 80

    # Membuat socket TCP/IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengikat socket ke alamat proxy server
    server.bind((proxy_host, proxy_port))

    # Mendengarkan koneksi masuk
    server.listen(5)

    print("[*] Proxy server listening on {}:{}".format(proxy_host, proxy_port))

    while True:
        # Menerima koneksi dari klien
        client_socket, addr = server.accept()

        print("[*] Accepted connection from {}:{}".format(addr[0], addr[1]))

        # Membuat thread untuk menangani koneksi dari klien
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()

if __name__ == "__main__":
    main()
