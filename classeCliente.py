import socket, threading, json
from time import gmtime, strftime, sleep
from random import random

def print_snapshot(state):
    print('SNAPSHOT!!!\nClients: {} \nEvents: {} \nSnapshotToken: {}'.format(
        state["clients"],
        state["events"],
        state["snapshot_token"]
    ))

#
# Classe com a lógica referente as interações do cliente
#
class Client (threading.Thread):
    def to_string(self):
        self.atualiza_saldo()
        return "Client {} - saldo {}".format(self.nome, self.saldo)
        
    def __str__(self):
        return self.to_string()
    def __unicode__(self):
        return self.to_string()
    def __repr__(self):
        return self.to_string()

        
    def __init__(self, csocket, caddres, localState, saldo = 0):
        threading.Thread.__init__(self)
        self.clientSocket = csocket
        self.clienteAddress = caddres
        self.nome = self.clientSocket.recv(4096).decode()
        self.doc = self.clientSocket.recv(4096).decode()
        with open('data.json') as f:
            data = json.load(f)
        self.saldo = data[self.nome][0]
        self.localState = localState
        
    def send(self, type, msg):
        self.clientSocket.sendall(type.encode())
        sleep(0.5)
        self.clientSocket.sendall(msg.encode())
        sleep(0.5)

    def run(self):
        print('Cliente {} de documento {} conectado através do IP {}.'.format(self.nome, self.doc, self.clienteAddress[0]))
        while True:
            snapshot_token = self.clientSocket.recv(4096).decode()
            msg = self.clientSocket.recv(4096).decode()
            content = msg
            
            #
            # Casos de interação do usuário disponíveis
            #
            if not msg:
                break
            elif msg == 'snapshot':
                self.localState["snapshot_token"] = str(random()) + "\r\n"
                print_snapshot(self.localState)
                for client in self.localState["clients"]:
                    try:
                        client.send("snapshot-token-updated", self.localState["snapshot_token"])
                    except Error as ex:
                        print(ex)
                        pass
                
            elif msg == 'saldo':
                print('Cliente {} solicitou visualizar o seu saldo.'.format(self.nome))
                self.send("saldo-resposta", self.verSaldo())
                content = '{} - {}'.format(msg, self.verSaldo())
                
            elif msg == 'deposito':
                print('Cliente {} deseja fazer um deposito. Aguardando o valor'. format(self.nome))
                valor = self.clientSocket.recv(4096).decode()
                self.deposito(int(valor))
                print('Valor de {} para deposito na conta de {}.'.format(valor, self.nome))
                self.send("deposito-resposta", self.verSaldo())
                content = '{} - {}'.format(msg, valor)
                
            elif msg == 'saque':
                print('Cliente {} deseja fazer um saque. Aguardando o valor'. format(self.nome))                
                valor = self.clientSocket.recv(4096).decode()
                result = self.saque(int(valor))
                content = '{} - {} - {}'.format(msg, valor, result)
                if(result == 'success'):
                    self.send(
                        "saque-resposta", 
                        'Saque realizado com sucesso. {}'.format(self.verSaldo())
                    )
                    print('Valor de {} para saque na conta de {}.'.format(valor, self.nome))
                else:
                    self.send(
                        "saque-resposta", 
                        str("Não é possível realizar essa operação: saldo insuficiente")
                    )
                    print('Error - Valor de {} para deposito na conta de {}.'.format(valor, self.nome))
                    
            elif msg == 'transferencia':
                nome_destinatario = self.clientSocket.recv(4096).decode()
                doc_destinatario = self.clientSocket.recv(4096).decode()
                valor = self.clientSocket.recv(4096).decode() 
                result = self.transferencia(int(valor), nome_destinatario)
                content = '{} - {} - {}'.format(msg, valor, result)
                if(result == 'success'):
                    self.send(
                        "transferencia-resposta", 
                        str("Transferência realizada com sucesso")
                    )
                else:
                    self.send(
                        "transferencia-resposta", 
                        str("Não é possível realizar essa operação: saldo insuficiente")
                    )
                print(msg)
                
            else:
                print(msg)
            
            if msg != 'snapshot' and self.localState["snapshot_token"] != snapshot_token:
                print("WRONG {}".format(snapshot_token))
                self.send('snapshot-token-updated', self.localState["snapshot_token"])
                print("Menagem recebida com snapshot-token antigo, regerando snapshot...")
                print_snapshot(self.localState)
                
            
            # self.clientSocket.send(self.localState["snapshot_token"].encode())
            self.localState["events"].append({ 
                "message": content, 
                "client" : self.nome, 
                "time": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())  
            })
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
