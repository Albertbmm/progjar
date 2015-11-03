import sys
import socket
import select
import pickle
import string

HOST = 'localhost' 
SOCKET_LIST = []
LIST_NAMA = []
RECV_BUFFER = 3999 
PORT = 12000


def chat_server():

	#sys.stdout.write('Port : ')
	#PORT = int(sys.stdin.readline())
	
	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# binding the socket
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)

	print "The chat server is started on Port " + str(PORT)
	#print "and the Host is " + str(HOST)

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
	  
		for sock in ready_to_read:
			# when new connection request received
			if sock == server_socket: 
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print "Client (%s, %s) is connected" % addr
				 
				broadcast(server_socket, sockfd, "[%s:%s] has joined the chat\n" % addr)
			 
			# a message from a client, not a new connection
			else:
				# process data received from client, 
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					#data = pickle.loads(data)
					if data:
						#broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
						temp1 = string.split(data[:-1])
				
						d=len(temp1)
						if temp1[0]=="login" :
							log_in(sock, str(temp1[1]))
								
						elif temp1[0]=="send" :
							
							logged = 0
							user = ""
							for x in range (len(LIST_NAMA)):
								if LIST_NAMA[x]==sock:
									logged=1
									user=LIST_NAMA[x+1]
							
							if logged==0:
								send_msg(sock, "Please login first\n")
							
							else:
								temp2=""
								for x in range (len(temp1)):
									if x>1:
										if not temp2:
											temp2+=str(temp1[x])
										else:
											temp2+=" "
											temp2+=str(temp1[x])
								
								for x in range (len(LIST_NAMA)):
									if LIST_NAMA[x]==temp1[1]:
										send_msg(LIST_NAMA[x-1], "["+user+"] : "+temp2+"\n")
				
						elif temp1[0]=="sendall" :
							
							logged = 0
							user = ""
							for x in range (len(LIST_NAMA)):
								if LIST_NAMA[x]==sock:
									logged=1
									user=LIST_NAMA[x+1]
							
							if logged==0:
								send_msg(sock, "Please login first\n")
							
							else:
								temp2=""
								for x in range(len(temp1)):
									if x!=0:
										if not temp2:
											temp2=str(temp1[x])
										else:
											temp2+=" "
											temp2+=temp1[x]
								broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n")
							
						elif temp1[0]=="list" :
							#send_msg(sock, "cobo\n")
							logged = 0
							for x in range (len(LIST_NAMA)):
								if LIST_NAMA[x]==sock:
									logged=1
							
							if logged==0:
								send_msg(sock, "Please login first\n")
							
							else:
								temp2=""
								for x in range (len(LIST_NAMA)):
									if x%2==1:
										temp2+=" "
										temp2+=str(LIST_NAMA[x])
								send_msg(sock, "[List_User] : "+temp2+"\n")
							
						
						else:
							print ('Invalid Command')
					else:
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

				# exception 
				except:
					broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
					continue

	server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for x in range (len(LIST_NAMA)):
		
        # send the message only to peer
        if LIST_NAMA[x] != server_socket and LIST_NAMA[x] != sock and x%2==0 :
            try :
                LIST_NAMA[x].send(message)
            except :
                # broken socket connection
                LIST_NAMA[x].close()
                # broken socket, remove it
                if LIST_NAMA[x] in SOCKET_LIST:
                    SOCKET_LIST.remove(LIST_NAMA[x])
 
def send_msg (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock)

def log_in (sock, user):
	g = 0
	f = 0
	for name in LIST_NAMA:
		if name == user:
			g = 1
		if name == sock:
			f = 1
	
	if f==1:
		send_msg(sock, "You already has a username\n")
	elif g==1:
		send_msg(sock, "Username already exist\n")
	else:
		LIST_NAMA.append(sock)
		LIST_NAMA.append(user)
		send_msg(sock, "Login success\n")
	
chat_server()
