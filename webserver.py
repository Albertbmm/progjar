import sys
import socket
import io


HOST, PORT = '', 8888
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
sock.bind((HOST,PORT))
sock.listen(1)
print 'starting up on port %s' % PORT
# sock.bind(server_address)

# Listen for incoming connections

while True:
    	connection, client_address = sock.accept()
        data = connection.recv(1024)
	gambarku = data.split()
	gambar1 =gambarku[1]	
	gambar2 =gambar1[1:]

	foto= open(gambar2+"foto.jpg",'r+')
	datagambar = foto.read()
	foto.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%datagambar


		# print >>sys.stderr, 'received "%s"' % data
            	# if data:
                #	print >>sys.stderr, 'sending data back to the client'
                #	connection.sendall(data)
            	# else:
                #	print >>sys.stderr, 'no more data from', client_address
                #	break
        # Clean up the connection
	connection.sendall(http_response)
	connection.close()
