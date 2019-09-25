from client import Client

cliente1 = Client('Joao', '123', 500)

cliente1.saque(300)
print(cliente1.saldo)