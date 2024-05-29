import socketserver

class ProxyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        remote_host = 'remote_server_ip_address'
        remote_port = 80
        
        # Membuat koneksi ke server tujuan
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
            remote_socket.connect((remote_host, remote_port))
            
            # Meneruskan data dari client ke server tujuan dan sebaliknya
            while True:
                # Menerima data dari client
                client_data = self.request.recv(4096)
                if not client_data:
                    break
                # Mengirim data dari client ke server tujuan
                remote_socket.sendall(client_data)
                
                # Menerima data dari server tujuan
                remote_data = remote_socket.recv(4096)
                if not remote_data:
                    break
                # Mengirim data dari server tujuan ke client
                self.request.sendall(remote_data)

class ProxyServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

def main():
    local_host = '127.0.0.1'
    local_port = 8888
    
    # Membuat server proxy dan menetapkan handler
    server = ProxyServer((local_host, local_port), ProxyHandler)
    print("[*] Listening on {}:{}".format(local_host, local_port))
    
    # Menjalankan server
    server.serve_forever()

if __name__ == "__main__":
    main()
  
