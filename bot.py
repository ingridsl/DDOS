from socket import *
serverName = 'DESKTOP-OOVUV0L' #Nome do meu computador na rede
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', clientPort))

serverSocket.listen(1)
clientSocket.send('cli'+gethostname())

while 1:
    connectionSocket = None
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