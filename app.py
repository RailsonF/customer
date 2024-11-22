#pegar uma senha (clientes)
#chamar uma senha (atendente)
#listar todas as senhas pendentes (ambos)

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

#classe para gerenciar filas de atendimento
class FilaAtendimento:
    def __init__(self):
        self.fila= [] #vai guardar todos os números da fila em ordem, para que quando for chamar, chame o primeiro
        self.proximo_numero = 1

    def gerar_senha(self):
        senha = self.proximo_numero
        self.fila.append(senha) #adicionou o que vai dar valor ao array fila
        self.proximo_numero += 1 #sempre adiciona um número a mais
        return senha 
    
    def atender_cliente(self):
        if self.fila: #se tem senha gerada para a fila (for verdadeiro)
            return self.fila.pop(0) #remova o número da posição 0, pois o cliente já está sendo atendido
        return None #se não tiver, não retorna nada 
    


class RequisicaoHandler(BaseHTTPRequestHandler):
    fila_atendimento = FilaAtendimento() #fila_atendimento recebe toda a classe

    def _set_headers(self, status=200): #serie de informações, nesse caso só está pedindo uma resposta do tipo json
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        #criar um endpoint (link) para gerar uma senha

    def do_POST(self): #ao clicar no link, vai gerar uma senha (metodo post de inserir algo)
        if self.path == "/senha": #se o caminho do link for igual a /senha, entrar na próxima linha
            senha = self.fila_atendimento.gerar_senha() #criou uma variável chamada chamar senha, e essa chama a variável fila de atendimento, que é uma classe, e nessa classe tem o método de gerar senha
            self._set_headers(201) #aqui fala que deu tudo certo, e chama o status 201 
            self.wfile.write(json.dumps({"senha": senha}).encode()) #aqui escreve a senha no formato json 
        else: #se não der certo chama o status 404 (not found)
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota não encontrada"}).encode())

    def do_GET(self):
        if self.path == "/chamar-senha":
            senha = self.fila_atendimento.atender_cliente()
            if senha:
                self._set_headers(200)
                self.wfile.write(json.dumps({"senha": senha}).encode())
            else:
                self._set_headers(204)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Rota não encontrada."}).encode())



def run():
    server_adress = ('', 8080)
    httpd = HTTPServer(server_adress, RequisicaoHandler)
    print("API rodando em http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
