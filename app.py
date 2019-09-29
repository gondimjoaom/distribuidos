#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

nome = input('Seja bem vindo ao Banco Gringotes, para comerçamos digite o seu nome de usuário: ')
client.send(nome.encode())
doc = input('Ótimo! Agora digite o seu documento: ')
client.send(doc.encode())

a = input('Qual operação você deseja realizar?: \n \
            Digite 1 para Saldo\n \
            Digite 2 para Depósito\n \
            Digite 3 para Saque\n \
            Digite 4 para transferência entre contas\n \
            Digite \"Encerrar\" para fechar o sistema!\n')
while a != 'Encerrar':
    if a == '1':
        client.send('saldo'.encode())
        print(client.recv(4096).decode())
    if a == '2':
        client.send('deposito'.encode())
        valor = input("\nQual o valor do depósito? \n")
        client.send(valor.encode())
        print('Depósito feito com sucesso. %s' %client.recv(4096).decode())
        pass
    if a == '3':
        client.send('saque'.encode())  
        valor = input("\nQual o valor do saque? \n")
        client.send(valor.encode()) 
        print(client.recv(4096).decode())                             
        pass
    if a == '4':
        pass

    a = input('\nQual outra operação você deseja realizar?: \n \
            Digite 1 para Saldo\n \
            Digite 2 para depósito\n \
            Digite 3 para saque\n \
            Digite 4 para transferência entre contas\n \
            Digite \"Encerrar\" para fechar o sistema!\n')
