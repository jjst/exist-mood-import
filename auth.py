from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import threading
import webbrowser

CLIENT_ID = '21c2af8828250ddc0fc5'

CODE = None

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        global CODE
        CODE = params['code'][0]
        self._set_headers()
        self.wfile.write(str.encode(
            "<html><body><h1>Authorization successful</h1><p>Authorization successful, you can close this page.</p></body></html>")
        )

    def do_HEAD(self):
        self._set_headers()

def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=9192):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.handle_request()
    httpd.socket.close()

def obtain_auth_code():
    webbrowser.open('https://exist.io/oauth2/authorize?response_type=code&client_id=%s&scope=%s' % (CLIENT_ID, "read+write"))
    run_server()
    return CODE
