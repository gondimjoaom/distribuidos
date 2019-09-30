import socket, threading, json
class Client (threading.Thread):
    def __init__(self, csocket, caddres, saldo = 0):
        threading.Thread.__init__(self)
        self.clientSocket = csocket
        self.clienteAddress = caddres
        self.nome = self.clientSocket.recv(4096).decode()
        self.doc = self.clientSocket.recv(4096).decode()
        self.saldo = saldo
        

    def run(self):
        print('Cliente {} conectado através do IP {}.'.format(self.nome, self.clienteAddress[0]))
        while True:
            msg = self.clientSocket.recv(4096).decode()
            if msg == 'xau' or not msg:
                break
            elif msg == 'saldo':
                print('Cliente {} solicitou visualizar o seu saldo.'.format(self.nome))
                self.clientSocket.send(self.verSaldo().encode())
            elif msg == 'deposito':
                print('Cliente {} deseja fazer um deposito. Aguardando o valor'. format(self.nome))
                valor = self.clientSocket.recv(4096).decode()
                print('Valor de {} para deposito na conta de {}.'.format(valor, self.nome))
                self.saldo += int(valor)
                self.clientSocket.send(self.verSaldo().encode())
            elif msg == 'saque':
                print(msg)
            elif msg == 'transferencia':
                print(msg)
            else:
                print(msg)
        print('{} desconectou.'.format(self.nome)) 
    
    def verSaldo(self):
        saldo = "\nSeu saldo é de R$" + str(self.saldo) + "."
        return saldo