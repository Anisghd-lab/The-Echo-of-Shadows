import http.server
import socketserver
import threading
import time

DIRECTORY = "/root/the_echo_of_shadows/web_preview"

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def serve_on_port(port):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), NoCacheHTTPRequestHandler) as httpd:
            print(f"L'Écho des Ombres server active on http://localhost:{port}", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server on port {port}: {e}", flush=True)

if __name__ == '__main__':
    t1 = threading.Thread(target=serve_on_port, args=(8088,), daemon=True)
    t1.start()
    print("Preview server started on http://localhost:8088")
    while True:
        time.sleep(1)
