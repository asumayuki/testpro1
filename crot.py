import socket
import ssl
import threading

def handle_client(client_socket):
    request = client_socket.recv(4096)

    # Tambahkan penanganan untuk HTTP
    if request.startswith(b'GET') or request.startswith(b'POST'):
        remote_host = 'localhost'
        remote_port = 3000
    # Tambahkan penanganan untuk DNS
    elif request[2:4] == b'\x01\x00':
        remote_host = '8.8.8.8'  # DNS server upstream
        remote_port = 53
    else:
        return

    # Tambahkan penanganan untuk TLS
    if remote_port == 443:
        client_socket = ssl.wrap_socket(client_socket, server_side=True)

    # Kirim permintaan ke server target
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((remote_host, remote_port))
    server_socket.send(request)

    # Teruskan respons dari server target ke klien
    while True:
        data = server_socket.recv(4096)
        if len(data) > 0:
            client_socket.send(data)
        else:
            break

    # Tutup koneksi
    server_socket.close()
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1234))  # Ganti dengan port TCP Anda
    server_socket.listen(5)

    print('Reverse proxy server running...')

    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
