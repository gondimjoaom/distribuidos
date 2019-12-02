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


operations = [
    ['saldo'],
    ['deposito', '500'],
    ['saldo'],
    ['saque', '400'],
    ['saldo']
]

while True:
  for operation in operations:
    client.sendall(localState["snapshot_token"].encode())
    time.sleep(1)
    for msg in operation:
      client.sendall(msg.encode())
      time.sleep(1)
