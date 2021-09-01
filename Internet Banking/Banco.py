from Conta import Conta

#Classe que representa o Banco e suas funcionalidades
class Banco():
    def __init__(self, codigo, conta, valor):
        self.codigo = codigo
        self.conta = conta
        self.valor = valor

    #Método que decide qual operação irá realizar
    def acao(self):
        if self.codigo == 1:
            return self.conta.saldo
        elif self.codigo == 2:
            return self.saque(self.valor)
        elif self.codigo == 3:
            return self.deposito(self.valor)

    #Função de saque
    def saque(self, valor):
        if valor > 0 and (self.conta.saldo - valor) >= 0:
            self.conta.saldo -= valor
            return self.conta.saldo
        else:
            return -1

    #Função de depósito
    def deposito(self, valor):
        if valor > 0:
            self.conta.saldo += valor
            return self.conta.saldo
        else:
            return -1