import http.server
import socketserver
import http.client

class ReverseProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Mengatur koneksi ke server tujuan
            target_host = "127.0.0.1"
            target_port = 80
            target_path = self.path
            target = http.client.HTTPConnection(target_host, target_port)
            target.request("GET", target_path)
            
            # Mendapatkan respons dari server tujuan
            response = target.getresponse()
            
            # Mengirim respons kembali ke client
            self.send_response(response.status)
            for header in response.getheaders():
                self.send_header(header[0], header[1])
            self.end_headers()
            self.wfile.write(response.read())
        except Exception as e:
            print("Error:", e)

# Menjalankan server pada port 8080
with socketserver.TCPServer(("localhost", 8080), ReverseProxy) as httpd:
    print("Reverse proxy berjalan di port 8080")
    httpd.serve_forever()
