# API Customer
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Create array of customers
customers = []
next_id = 1

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        # Lista todos os clientes
        if self.path == "/clientes":
            self._send_response(200, customers)
        # Retorna 404 para outras rotas GET não implementadas
        else:
            self._send_response(404, {"message": "Rota não encontrada."})

    def do_POST(self):
        global next_id
        # Cria um novo cliente
        if self.path == "/clientes":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            cliente_data = json.loads(body)
            cliente_data['id'] = next_id
            next_id += 1
            customers.append(cliente_data)
            self._send_response(201, cliente_data)
        else:
            self._send_response(404, {"message": "Rota não encontrada."})
            
# Inicialização do servidor
def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("API rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
