from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client

class ReverseProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Ganti URL tujuan dengan yang Anda inginkan
        destination_url = "http://example.com" + self.path
        
        # Membuat koneksi ke server tujuan
        destination = http.client.HTTPConnection("example.com")
        destination.request("GET", self.path, headers=self.headers)
        
        # Mendapatkan respons dari server tujuan
        response = destination.getresponse()
        
        # Mengirim respons ke klien
        self.send_response(response.status)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.read())

if __name__ == "__main__":
    server_address = ('', 8000)  # Ganti dengan port yang diinginkan
    httpd = HTTPServer(server_address, ReverseProxyHandler)
    print("Reverse proxy berjalan di port 8000...")
    httpd.serve_forever()
