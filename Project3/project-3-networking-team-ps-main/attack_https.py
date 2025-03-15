import subprocess
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys


known_aes_key = "4d6167696320576f7264733a2053717565616d697368204f7373696672616765"

class KeyServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Custom HTML response with the known AES key
        attack_payload = (
            "<html>\n<head>\n  <title>Free AES Key Generator!</title>\n</head>\n"
            "<body>\n<h1 style=\"margin-bottom: 0px\">Free AES Key Generator!</h1>"
            "<span style=\"font-size: 5%\">Definitely not run by the NSA.</span><br/>\n"
            "<br/><br/>Your <i>free</i> AES-256 key: <b>{}</b><br/>\n"
            "</body></html>"
        ).format(known_aes_key)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(attack_payload.encode())

def setup_iptables():
    print("Setting up iptables rule...")
    subprocess.run([
        "sudo", "iptables", "-t", "nat", "-A", "OUTPUT",
        "-p", "tcp", "-d", "freeaeskey.xyz", "--dport", "443",
        "-j", "DNAT", "--to-destination", "127.0.0.1:443"
    ])

def cleanup_iptables():
    print("Cleaning up iptables rule...")
    subprocess.run([
        "sudo", "iptables", "-t", "nat", "-D", "OUTPUT",
        "-p", "tcp", "-d", "freeaeskey.xyz", "--dport", "443",
        "-j", "DNAT", "--to-destination", "127.0.0.1:443"
    ])

def run_server():
    def signal_handler(sig, frame):
        print("\nShutting down server...")
        cleanup_iptables()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    httpd = HTTPServer(('localhost', 443), KeyServerHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Serving HTTPS on port 443...")

    
    try:
        httpd.serve_forever()
    finally:
        cleanup_iptables()

if __name__ == "__main__":
    setup_iptables()
    run_server()

