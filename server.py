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

while 1:
	data, addr = sock.recvfrom(512)
	print(data)
