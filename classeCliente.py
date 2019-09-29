#!/usr/bin/python
# -*- coding: utf-8 -*-

class Client (object):
    def __init__(self, nome, doc, saldo = 0):
        self.nome = nome
        self.doc = doc
        self.saldo = saldo
    
    def verSaldo (self):
        saldo = "Seu saldo é de R$" + str(self.saldo) + "."
        return saldo
