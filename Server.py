# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.xml with the following command:
#    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:4443
#    https://127.0.0.1:4443/

#to configure apache: https://www.digitalocean.com/community/tutorials/como-configurar-apache-virtual-hosts-no-ubuntu-16-04-pt

import BaseHTTPServer, SimpleHTTPServer
import ssl

print 'Servidor pronto'
print 'https://localhost:4443'
print 'https://127.0.0.1:4443'

httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()
