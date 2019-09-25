from classeCliente import Client
from xmlrpc.server import SimpleXMLRPCServer

quit = 0
def kill():
    global quit
    quit = 1
    return 1

def verSaldo(nome, doc):
    for cliente in clientes:
        if (cliente.nome == nome and cliente.doc == doc):
            return cliente.verSaldo()
def deposito(nome, doc, valor):
    for cliente in clientes:
        if (cliente.nome == nome and cliente.doc == doc):
            cliente.saldo += valor

cliente1 = Client('Joao', '123', 500)

clientes = []

clientes.append(cliente1)

server = SimpleXMLRPCServer(("127.0.0.2", 8000), allow_none=True)
print("Banco Gringotes iniciado e escutando na porta 8000")
server.register_function(kill)
server.register_function(verSaldo)
server.register_function(deposito)

while not quit:
    server.handle_request()