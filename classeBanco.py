from classeCliente import Client
import socket

def verSaldo(nome, doc):
    for cliente in clientes:
        if (cliente.nome == nome and cliente.doc == doc):
            return cliente.verSaldo().encode()
def deposito(nome, doc, valor):
    for cliente in clientes:
        if (cliente.nome == nome and cliente.doc == doc):
            cliente.saldo += valor

def sendString(msg):
    return conn.send(msg.encode())

cliente1 = Client('Joao', '123', 500)

clientes = []

clientes.append(cliente1)

#estabelecendo conexão
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.7', 8000))
server.listen(5)

print("Banco Gringotes iniciado e escutando na porta 8000")

conn, add = server.accept()

clienteNome = conn.recv(4096).decode()
clienteDoc = conn.recv(4096).decode()
print('Cliente {}, de documento {}, se conectou usando o IP {} com nome {}.'.format(clienteNome, clienteDoc,add[0],socket.gethostbyaddr(add[0])[0]))

while True:
    data = conn.recv(4096).decode()
    if data == 'saldo':
        conn.send(verSaldo(clienteNome, clienteDoc))
    elif data == 'deposito':
        valor = conn.recv(4096).decode()
        deposito(clienteNome, clienteDoc, int(valor))
        conn.send(verSaldo(clienteNome, clienteDoc))
    elif not data:
        break

server.close()