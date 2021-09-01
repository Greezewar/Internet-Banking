#Classe para representar uma conta do banco
class Conta():
    def __init__(self, usuario, senha, logado, saldo):
        self.usuario = usuario
        self.senha = senha
        self.logado = logado
        self.saldo = saldo