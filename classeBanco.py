#!/usr/bin/python
# -*- coding: utf-8 -*-

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
def saque(nome, doc, valor):
    for cliente in clientes:
        if (cliente.nome == nome and cliente.doc == doc):
            if(cliente.saldo < valor):
                return 'error'
            cliente.saldo -= valor
            return 'success'
def transferencia(nome, doc, valor, nome_destinatario, doc_destinatario):
    result = saque(nome, doc, int(valor))
    if(result == 'success'):
        deposito(nome_destinatario, doc_destinatario, int(valor))
        return 'success' 
    else:
        return 'error'
            

def sendString(msg):
    return conn.send(msg.encode())

cliente1 = Client('Joao', '123', 500)
cliente2 = Client('Paula', '321', 1000)

clientes = []

clientes.append(cliente1)
clientes.append(cliente2)

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
    elif data == 'saque':
        valor = conn.recv(4096).decode()
        result = saque(clienteNome, clienteDoc, int(valor))
        if(result == 'success'):
            conn.send(verSaldo(clienteNome, clienteDoc))
        else:
            conn.send(str("Não é possível realizar essa operação: saldo insuficiente").encode())
    elif data == 'transferencia':
        nome_destinatario = conn.recv(4096).decode()
        doc_destinatario = conn.recv(4096).decode()
        valor = conn.recv(4096).decode() 
        result = transferencia(clienteNome, clienteDoc, int(valor), nome_destinatario, doc_destinatario)
        if(result == 'success'):
            conn.send(str("Transferência realizada com sucesso").encode())
        else:
            conn.send(str("Não é possível realizar essa operação: saldo insuficiente").encode())          
    elif not data:
        break

server.close()
