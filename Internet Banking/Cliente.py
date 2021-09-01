from PySimpleGUI import *
import socket

class Client():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.size = 1024
		self.main()

	#Interface de login
	def login(self, client):
		layout = [[Text('Usuário')], 
		[Input(key = 'USUARIO')], 
		[Text('Senha')], 
		[Input(key = 'SENHA', password_char = '*')], 
		[Text(size = (40, 1), key = 'STATUS')], 
		[Button('Entrar'), Button('Sair')]]

		window = Window('Login', layout)

		while True:
			event, values = window.read()

			#Envia dados de acesso
			if event == 'Entrar':
				if values['USUARIO'] != '' and values['SENHA'] != '':
					client.send(values['USUARIO'].encode('ascii'))
					print()
					client.send(values['SENHA'].encode('ascii'))

					#Recebe código de acesso
					resposta = client.recv(self.size)
					resposta = str(resposta.decode('ascii'))

					if resposta == '98':
						window['STATUS'].update('Logado com sucesso!')
						window.close()
						self.menu(client)
					else:
						window['STATUS'].update('Usuário já logado ou dados incorretos, tente novamente.')
				else:
					window['STATUS'].update('Os campos de usuário e senha devem ser preenchidos.')
			elif event == 'Sair' or event == WIN_CLOSED:
				break

		window.close() 

	#Interface de menu
	def menu(self, client):
		layout = [[Text('O que deseja fazer?')],
		[Button('Verificar saldo'), Button('Saque'), Button('Depósito')],
		[Button('Sair')]]

		window = Window('Menu', layout)

		while True:
			event, values = window.read()

			if event == 'Verificar saldo':
				window.close()
				self.saldo(client)
			elif event == 'Saque':
				window.close()
				self.saque(client)
			elif event == 'Depósito':
				window.close()
				self.deposito(client)
			elif event == 'Sair' or event == WIN_CLOSED:
				break
		
		window.close()

	#Interface de verificar saldo
	def saldo(self, client):
		operacao = '1'
		client.send(operacao.encode('ascii'))
		resposta = client.recv(self.size)

		layout = [[Text('Saldo atual:')],
		[Text('R$ ' + str(resposta.decode('ascii')))],
		[Button('Voltar')]]

		window = Window('Saldo', layout)

		while True:
			event, values = window.read()

			if event == 'Voltar' or event == WIN_CLOSED:
				break

		window.close()
		self.menu(client)

	#Interface de saque
	def saque(self, client):
		layout = [[Text('Informe abaixo, o valor que deseja sacar.')],
		[Input(key = 'VALOR')],
		[Text(size = (40, 1), key = 'STATUS')],
		[Button('Confirmar'), Button('Voltar')]]

		window = Window('Saque', layout)

		while True:
			event, values = window.read()

			if event == 'Confirmar':
				if values['VALOR'] != '':
					operacao = '2'
					client.send(operacao.encode('ascii'))
					print()
					client.send(values['VALOR'].encode('ascii'))
					resposta = client.recv(self.size)

					if resposta.decode('ascii') == '-1':
						window['STATUS'].update('Saldo insuficiente. Tente novamente.')
					else:
						window['STATUS'].update('Saque efetuado com sucesso!')
						window.close()
						self.menu(client)
				else:
					window['STATUS'].update('Por favor, informe o valor desejado.')
			elif event == 'Voltar' or event == WIN_CLOSED:
				break

		window.close()
		self.menu(client)

	#Interface de depósito
	def deposito(self, client):
		layout = [[Text('Informe abaixo, o valor que deseja depositar.')],
		[Input(key = 'VALOR')],
		[Text(size = (40, 1), key = 'STATUS')],
		[Button('Confirmar'), Button('Voltar')]]

		window = Window('Depósito', layout)

		while True:
			event, values = window.read()

			if event == 'Confirmar':
				if values['VALOR'] != '':
					operacao = '3'
					client.send(operacao.encode('ascii'))
					print()
					client.send(values['VALOR'].encode('ascii'))
					resposta = client.recv(self.size)

					if resposta.decode('ascii') == '-1':
						window['STATUS'].update('Valor inválido. Tente novamente.')
					else:
						window['STATUS'].update('Depósito efetuado com sucesso!')
						window.close()
						self.menu(client)
				else:
					window['STATUS'].update('Por favor, informe o valor desejado.')
			elif event == 'Voltar' or event == WIN_CLOSED:
				break

		window.close()
		self.menu(client)

	#Método principal
	def main(self):	
		#Conexão com o servidor
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
		client.connect((self.host, self.port))
		
		#Chama a interface
		self.login(client)
		#Finaliza a conexão
		client.close()

Client('127.0.0.1', 7000)