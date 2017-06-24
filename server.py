#para testar: 
#-um terminal executar 'sudo python server.py'
#-o outro 'dig howcode.org @127.0.0.1
#ou qualquer outro endereco no lugar de howcode.org


import socket
port = 53
ip = '127.0.0.1'
#meu endereco de ip

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def buildresponse(data): #DNS Header

	#Transaction ID
	TransactionID = data[0:2]
	TID = ''
	for byte in TransactionID
		TID += hex(byte)[2:]
	#print(TID)
	
	#Flags
	Flags = getflags(data[2:4])
while 1:
	data, addr = sock.recvfrom(512)
	#print(data)
	r = buildresponse(data)
	sock.sendto(r, addr)
