#!/usr/bin/python
# -*- coding: utf-8 -*-

from classeCliente import Client
import socket, threading, json

#
# Estabelecendo conexão
#
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))

print("Banco Gringotes iniciado e escutando na porta 8000")

#
# Manter o server ativo através de threading
#
while True:
    server.listen(1)
    conn, add = server.accept()
    newCliente = Client(conn, add)
    newCliente.start()
