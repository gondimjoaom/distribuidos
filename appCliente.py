#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
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

localState = {
    "snapshot_token": '-'
}

def message_handler():
    while True:
        msg = client.recv(4096)
        if not msg:
            pass
        msg = msg.decode()
        
        if msg == 'snapshot-token-updated':
            localState["snapshot_token"] = client.recv(4096).decode()
            print("Novo token de snapshot é {}".format(localState["snapshot_token"]))
            pass
        elif msg == 'saldo-resposta':
            print(client.recv(4096).decode())
            pass
        elif msg == 'deposito-resposta':
            response = client.recv(4096).decode()
            print('Depósito feito com sucesso. %s' % response)
            pass
        elif msg == 'saque-resposta':
            print(client.recv(4096).decode())                             
            pass
        elif msg == 'transferencia-resposta':
            print(client.recv(4096).decode())
            pass
        elif msg == 'novo-snapshot':
            print(client.recv(4096).decode())
            pass

thread = threading.Thread(target = message_handler)
thread.start()

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
    client.send(localState["snapshot_token"].encode())
    time.sleep(1)
    if a == '1':
        client.send('saldo'.encode())
    elif a == '2':
        client.send('deposito'.encode())
        valor = input("\nQual o valor do depósito? \n")
        client.send(valor.encode())
        pass
    elif a == '3':
        client.send('saque'.encode())  
        valor = input("\nQual o valor do saque? \n")
        client.send(valor.encode())                          
        pass
    elif a == '4':
        client.send('transferencia'.encode())  
        nome_destinatario = input("\nQual o nome do destinatário? \n")
        client.send(nome_destinatario.encode())            
        doc_destinatario = input("\nQual o documento do destinatário? \n") 
        client.send(doc_destinatario.encode())         
        valor = input("\nQual o valor da tranferência? \n")
        client.send(valor.encode())
        pass
    elif a == 'snapshot':
        client.send('snapshot'.encode())
        pass
    else:
        client.send('comando-desconhecido'.encode())

    a = input('\nQual outra operação você deseja realizar?: \n \
            Digite 1 para Saldo\n \
            Digite 2 para depósito\n \
            Digite 3 para saque\n \
            Digite 4 para transferência entre contas\n \
            Digite \"Encerrar\" para fechar o sistema!\n')
