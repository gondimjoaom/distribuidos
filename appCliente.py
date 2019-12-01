#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time

#
# Conexão com o servidor
#
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

#
# Inputs iniciais
#
nome = input('Seja bem vindo ao Banco Gringotes, para comerçamos digite o seu nome de usuário: ')
client.send(nome.encode())
doc = input('Ótimo! Agora digite o seu documento: ')
client.send(doc.encode())

snapshot_token = "-"

#
# Opções de interação com o servidor
#
a = input('Qual operação você deseja realizar?: \n \
            Digite 1 para Saldo\n \
            Digite 2 para Depósito\n \
            Digite 3 para Saque\n \
            Digite 4 para transferência entre contas\n \
            Digite \"Encerrar\" para fechar o sistema!\n')
while a != 'Encerrar':
    client.send(snapshot_token.encode())
    if a == '1':
        client.send('saldo'.encode())
        print(client.recv(4096).decode())
    if a == '2':
        client.send('deposito'.encode())
        valor = input("\nQual o valor do depósito? \n")
        client.send(valor.encode())
        response = client.recv(4096).decode()
        print('Depósito feito com sucesso. %s' % response)
        pass
    if a == '3':
        client.send('saque'.encode())  
        valor = input("\nQual o valor do saque? \n")
        client.send(valor.encode()) 
        print(client.recv(4096).decode())                             
        pass
    if a == '4':
        client.send('transferencia'.encode())  
        nome_destinatario = input("\nQual o nome do destinatário? \n")
        client.send(nome_destinatario.encode())            
        doc_destinatario = input("\nQual o documento do destinatário? \n") 
        client.send(doc_destinatario.encode())         
        valor = input("\nQual o valor da tranferência? \n")
        client.send(valor.encode())
        print(client.recv(4096).decode())
        pass
    if a == 'snapshot':
        client.send('snapshot'.encode())
        client.recv(4096)
        pass
        
        
    #print(client.recv(4096))

    a = input('\nQual outra operação você deseja realizar?: \n \
            Digite 1 para Saldo\n \
            Digite 2 para depósito\n \
            Digite 3 para saque\n \
            Digite 4 para transferência entre contas\n \
            Digite \"Encerrar\" para fechar o sistema!\n')
