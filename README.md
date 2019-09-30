# trabalho de Distribuídos

#### Fazer:

- [ ] Juntar classes classeBanco e classeCliente em um arquivo que vai rodar o programa;
- [ ] Implementar sockets em python para abrir em dois terminais diferentes inicialmente;
  - [ ] depois podemos **tentar** colocar entre duas máquinas, mas acho difícil na rede UFBA
- [ ] Saber quais são as impedições que o sistema precisa ter para não ocorrerem dois saques em uma mesma conta tirando mais dinheiro do que deveria ou algo do tipo
  - isso pode ser feito com algo tipo mutex ou semáforos em python (eu acho).

#### Procurar saber do professor:

- Os clientes devem ser salvos em algum arquivo para poder fechar e abrir o programa com estados salvos ou pode ser tudo salvo em memória conforme o programa roda?

#### Links úteis:

- https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client talvez possa ajudar a usar RPC
- https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server lado server
- https://stackoverflow.com/questions/3310049/proper-use-of-mutexes-in-python
- https://stackoverflow.com/questions/31508574/semaphores-on-python esse link pode ser bastante útil!!
- https://www.pubnub.com/blog/socket-programming-in-python-client-server-p2p/

#### Como executar:

1 - Ativar ambiente virtual""

```

source banco_socket/bin/activate

```

2 - Executar o arquivo `classeBanco.py` para iniciar o servidor do banco:

```
python classeBanco.py

```

3 - Executar o arquivo `app.py` para executar a aplicação do cliente:

```
python app.py

```
