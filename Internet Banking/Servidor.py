import socket
import threading
from Banco import Banco
from Conta import Conta

#Classe para realizar a conexão entre servidor e cliente
class ThreadedServer():
    def __init__(self, host, port, array):
        self.host = host
        self.port = port
        self.size = 1024
        self.array = array
        self.listen()
    
    #Método para iniciar o server
    def listen(self):      
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        print('Conexão aberta na porta', self.port)
        sock.listen(3) #Número máximo de conexões simultâneas
        print('Esperando conexão')

        #Loop infinito que espera conexão e cria novas Threads
        while True:          
            client, address = sock.accept()
            print('Conectado a:', address[0], ':', address[1])
            threading.Thread(target = self.verify, args = (client, address)).start()

    #Método para escutar o cliente
    def listenToClient(self, client, address, account):
        while True:
            try:
                data = client.recv(self.size)
                if data: 
                    self.operation(int(data.decode('ascii')), client, address, account)
                else:
                    raise socket.error('Cliente disconectado')
            except:
                client.close()
                return False

    #Método para determinar a função a ser utilizada
    def operation(self, code, client, address, account):
        #Consulta de saldo
        if code == 1:
            banco = Banco(1, account, 0)
            client.send(str(banco.acao()).encode('ascii'))
        #Saque
        elif code == 2:
            valor = client.recv(self.size)
            banco = Banco(2, account, int(valor.decode('ascii')))
            client.send(str(banco.acao()).encode('ascii'))
        #Depósito
        elif code == 3:
            valor = client.recv(self.size)
            banco = Banco(3, account, int(valor.decode('ascii')))
            client.send(str(banco.acao()).encode('ascii'))

    #Método para realizar a autenticação do cliente
    def autentication(self, usuario, senha):
        resp = None
        for i in array:
            if i.logado == False and i.usuario == usuario and i.senha == senha:
                i.logado = True
                return i
        return resp

    #Método para receber usuário e senha do cliente
    def verify(self, client, address): 
        account = None
        while True:
            try:
                data = client.recv(self.size)
                usuario = data.decode('ascii')

                data = client.recv(self.size)
                senha = data.decode('ascii')
                
                if usuario and senha:
                    account = self.autentication(usuario, senha)
                    if account != None:
                        data = '98'
                        client.send(data.encode('ascii'))
                        self.listenToClient(client, address, account)
                    else:
                        data = '99'
                        client.send(data.encode('ascii'))
                else:
                    raise socket.error('Cliente disconectado')
            except:
                if account != None:
                    account.logado = False
                    
                client.close()
                return False

array = [Conta('admin', 'admin', False, 5000.00), Conta('usuario1', 'senha1', False, 2000.00), Conta('usuario2', 'senha2', False, 3000.00)]
ThreadedServer('', 7000, array)