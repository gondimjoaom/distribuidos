#!/usr/bin/python
# -*- coding: utf-8 -*-

from classeCliente import Client
import socket, threading, json

#estabelecendo conexão
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))

print("Banco Gringotes iniciado e escutando na porta 8000")


while True:
    with open('data.json') as f:
        data = json.load(f)
    print(data)
    #with open('data.json', 'w') as out:
    #    json.dump(data, out)
    server.listen(1)
    conn, add = server.accept()
    newCliente = Client(conn, add)
    newCliente.start()
