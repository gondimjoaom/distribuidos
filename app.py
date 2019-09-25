import xmlrpc.client
nome = input('Seja bem vindo ao Banco Gringotes, para comerçamos digite o seu nome de usuário: ')
doc = input('Ótimo! Agora digite o seu documento: ')
with xmlrpc.client.ServerProxy("http://127.0.0.2:8000/") as proxy:
    a = input('Qual operação você deseja realizar?: \n \
                Digite 1 para Saldo\n \
                Digite 2 para Saque\n \
                Digite 3 para depósito\n \
                Digite 4 para transferência entre contas\n \
                Digite \"Encerrar\" para fechar o sistema!\n')
    while a != 'Encerrar':
        if a == '1':
            print(proxy.verSaldo(nome, doc))
        if a == '2':
            valor = int(input("\nQual o valor do depósito? \n"))
            proxy.deposito(nome, doc, valor)
            print('Deposito feito com sucesso. %s' %proxy.verSaldo(nome, doc))
            pass
        if a == '3':
            pass
        if a == '4':
            pass        

        a = input('\nQual outra operação você deseja realizar?: \n \
                Digite 1 para Saldo\n \
                Digite 2 para Saque\n \
                Digite 3 para depósito\n \
                Digite 4 para transferência entre contas\n \
                Digite \"Encerrar\" para fechar o sistema!\n')
    proxy.kill()