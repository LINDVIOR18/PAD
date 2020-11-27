from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
'''listening to incoming requests'''


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self, body=True):
        try:
            # Parse request
            hostname = '127.0.0.1:5000'
            url = 'https://{}'.format(hostname)
            req_header = self.parse_headers()

            # Call the target service
            resp = requests.get(url, headers=req_header, verify=False)

            # Respond with the requested data
            self.send_response(resp.status_code)
            self.send_resp_headers(resp.headers)
            self.wfile.write(resp.content)

        finally:
            self.finish()


    def parse_headers(self):
        req_header = {}
        for line in self.headers.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8082)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()
