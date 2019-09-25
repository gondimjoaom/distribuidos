class Client (object):
    def __init__(self, nome, doc, saldo = 0):
        self.nome = nome
        self.doc = doc
        self.saldo = saldo

    def saque (self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            print('Saque de R$' + str(valor) + ' realizado com sucesso.')

    def deposito (self, valor):
        self.saldo += valor
    
    def verSaldo (self):
        print("Seu saldo é de R$" + str(self.saldo) + ".")

    