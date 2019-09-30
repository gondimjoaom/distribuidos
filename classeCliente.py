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
                self.deposito(int(valor))
                print('Valor de {} para deposito na conta de {}.'.format(valor, self.nome))
                self.clientSocket.send(self.verSaldo().encode())
            elif msg == 'saque':
                print('Cliente {} deseja fazer um saque. Aguardando o valor'. format(self.nome))                
                valor = self.clientSocket.recv(4096).decode()
                result = self.saque(int(valor))
                if(result == 'success'):
                    self.clientSocket.send('Saque realizado com sucesso. {}'.format(self.verSaldo()).encode())
                    print('Valor de {} para saque na conta de {}.'.format(valor, self.nome))                    
                else:
                    self.clientSocket.send(str("Não é possível realizar essa operação: saldo insuficiente").encode())
                    print('Error - Valor de {} para deposito na conta de {}.'.format(valor, self.nome))
            elif msg == 'transferencia':
                nome_destinatario = self.clientSocket.recv(4096).decode()
                doc_destinatario = self.clientSocket.recv(4096).decode()
                valor = self.clientSocket.recv(4096).decode() 
                result = self.transferencia(int(valor), nome_destinatario, doc_destinatario)
                if(result == 'success'):
                    self.clientSocket.send(str("Transferência realizada com sucesso").encode())
                else:
                    self.clientSocket.send(str("Não é possível realizar essa operação: saldo insuficiente").encode())
                print(msg)
            else:
                print(msg)
        print('{} desconectou.'.format(self.nome)) 
    
    def verSaldo(self):
        saldo = "\nSeu saldo é de R$" + str(self.saldo) + "."
        return saldo
        
    def deposito(self, valor):
        self.saldo += int(valor)
            
    def saque(self, valor):
        if(self.saldo < valor):
            return 'error'
        self.saldo -= valor
        return 'success'
                
    def transferencia(self, valor, nome_destinatario, doc_destinatario):
        result = self.saque(valor)
        if(result == 'success'):
            # Implementar deposito para transferência
            return 'success' 
        else:
            return 'error'
