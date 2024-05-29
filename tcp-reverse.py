import socket
import threading

def handle_client(client_socket, target_host, target_port):
    # Connect to the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    # Forward data between client and target
    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if len(client_data) == 0:
            break
        # Send received data to the target
        target_socket.send(client_data)

        # Receive data from the target
        target_data = target_socket.recv(4096)
        if len(target_data) == 0:
            break
        # Send received data back to the client
        client_socket.send(target_data)

    # Close the connections
    client_socket.close()
    target_socket.close()

def run_proxy(listen_host, listen_port, target_host, target_port):
    # Create the listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(5)

    print(f'Reverse proxy is listening on {listen_host}:{listen_port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr[0]}:{addr[1]}')

        # Create a thread to handle the client connection
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()

if __name__ == '__main__':
    listen_host = '0.0.0.0'  # Mendengarkan semua alamat IP yang tersedia
    listen_port = 8888       # Port untuk menerima koneksi dari klien
    target_host = 'example.com'  # Ganti dengan alamat IP atau nama host target
    target_port = 80          # Port untuk meneruskan koneksi ke target

    run_proxy(listen_host, listen_port, target_host, target_port)
