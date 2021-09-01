from PySimpleGUI import *

#Dados de login
usuario = 'admin'
senha = 'admin'

#Define the window's contents
layout = [[Text('Usuário')], [Input(key = 'USUARIO')], [Text('Senha')], [Input(key = 'SENHA', password_char = '*')], [Text(size = (40, 1), key = 'STATUS')], [Button('Entrar'), Button('Sair')]]

#Create the window
window = Window('Login', layout)

#Display and interact with the Window
while True:
    event, values = window.read()

    #See if user wants to quit or window was closed
    if event == 'Entrar':
        #Output a message to the window
        if values['USUARIO'] == usuario and values['SENHA'] == senha:
            window['STATUS'].update('Logado com sucesso!')
        else:
            window['STATUS'].update('Usuário ou senha incorretos.')
    elif event == 'Sair' or WINDOW_CLOSED:
        break

#Finish up by removing from the screen
window.close() 