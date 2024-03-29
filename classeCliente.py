import socket, threading, json
#
# Classe com a lógica referente as interações do cliente
#
class Client (threading.Thread):
    def __init__(self, csocket, caddres, saldo = 0):
        threading.Thread.__init__(self)
        self.clientSocket = csocket
        self.clienteAddress = caddres
        self.nome = self.clientSocket.recv(4096).decode()
        self.doc = self.clientSocket.recv(4096).decode()
        with open('data.json') as f:
            data = json.load(f)
        self.saldo = data[self.nome][0]
        

    def run(self):
        print('Cliente {} de documento {} conectado através do IP {}.'.format(self.nome, self.doc, self.clienteAddress[0]))
        while True:
            msg = self.clientSocket.recv(4096).decode()
            #
            # Casos de interação do usuário disponíveis
            #
            if not msg:
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
                result = self.transferencia(int(valor), nome_destinatario)
                if(result == 'success'):
                    self.clientSocket.send(str("Transferência realizada com sucesso").encode())
                else:
                    self.clientSocket.send(str("Não é possível realizar essa operação: saldo insuficiente").encode())
                print(msg)
                
            else:
                print(msg)
        print('{} desconectou.'.format(self.nome)) 
    
    # Função
    # Verifica o saldo do usuário logado
    #
    def verSaldo(self):
        self.atualiza_saldo()
        saldo = "\nSeu saldo é de R$" + str(self.saldo) + "."
        return saldo
    
    # Função
    # Faz depósito na conta do usuário logado
    #
    def deposito(self, valor):
        self.saldo += int(valor)
        self.altera_saldo(self.nome, self.saldo)
    
    # Função
    # Realiza saque na conta do usuário logado
    #
    def saque(self, valor):
        self.atualiza_saldo()        
        if(self.saldo < valor):
            return 'error'
        self.saldo -= valor
        self.altera_saldo(self.nome, self.saldo)        
        return 'success'
    
    # Função
    # Realiza transferência da conta logada para outrem
    #     
    def transferencia(self, valor, nome_destinatario):
        self.atualiza_saldo()        
        result = self.saque(valor)
        nome = nome_destinatario
        if(result == 'success'):
            with open('data.json') as f:
                data = json.load(f)
                saldo = data[nome_destinatario][0] + int(valor)
                self.altera_saldo(nome, saldo)
            return 'success' 
        else:
            return 'error'
    
    # Função
    # Altera o saldo de conta passada por parâmetro
    # 
    def altera_saldo(self, nome, saldo):
        self.atualiza_saldo()        
        with open('data.json') as f:
            data = json.load(f)
            data[nome][0] = saldo
        with open('data.json', 'w') as out:
            json.dump(data, out)  
    
    # Função
    # Atuliza o saldo antes de operações
    # 
    def atualiza_saldo(self):
        with open('data.json') as f:
            data = json.load(f)
        self.saldo = data[self.nome][0]
