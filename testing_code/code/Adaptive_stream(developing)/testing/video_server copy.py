
# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64
import struct
import pickle

#buffer
BUFF_SIZE1 = 65536
BUFF_SIZE2 = 65536
BUFF_SIZE3 = 65536


##_____initializing socket1______##
server_socket1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE1)
#_____________________________________________________________________#
##_____initializing socket2______##
server_socket2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket2.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE2)
#_____________________________________________________________________#
##_____initializing socket3______##
server_socket3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket3.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE3)
#_____________________________________________________________________#



host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
print(host_ip)


port1 = 9999
port2 = 9998
port3 = 9997



socket_address1 = (host_ip,port1)
server_socket1.bind(socket_address1)
print('Listening at:',socket_address1)

socket_address2 = (host_ip,port2)
server_socket2.bind(socket_address2)
print('Listening at:',socket_address2)

socket_address3 = (host_ip,port3)
server_socket3.bind(socket_address3)
print('Listening at:',socket_address3)


vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)
i, j, k, l, m, n, o= 0, 0, 0, 0, 0, 0, 0
FPS = 'waiting...'
change = b''


while True:

	
	msg1,client_addr1 = server_socket1.recvfrom(BUFF_SIZE1)
	print('GOT connection from ',client_addr1, msg1)

	while(vid.isOpened()):

		###Adds iteration every time this loop is run and takes
		###in value from port2 of client###
		msg2,client_addr2 = server_socket2.recvfrom(BUFF_SIZE2)
		#print('GOT connection from ',client_addr2)
		#print('Received from || UDP: %s', msg2)
		parameters = (pickle.loads(msg2))

		x = int(parameters[0])	# the image quality
		y = int(parameters[1])	# the image width
	
	
	 ##################################################################
		###PORT 3 is used to get framerate #############
		
		msg3,client_addr3 = server_socket3.recvfrom(BUFF_SIZE3)

		#print('GOT connection from ',client_addr3)
		#print('Received from || UDP: %s', msg3)
		
		if msg3.startswith(b'int'):
			# assumes 4 byte unsigned integer
			received1 = struct.unpack('!I', msg3[-4:])[0]
		else:
			received1 = msg3.decode('utf-8')
		#print (repr(msg3))  # for debug purposes
		feedback_fps=int(received1)

		i=0
		j+=1  #counting eedback iteraitions
		#print("Feedback Interations :", j)
		#############################
		quality =x
		WIDTH= y



		#while(vid.isOpened()): # moved thisloop up above
		while(i<=2): #checks feedback fromclient after every 50 frames.
			
			_,frame = vid.read()
			frame = imutils.resize(frame,width=WIDTH)
			encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,quality])
			message = base64.b64encode(buffer)
			server_socket1.sendto(message,client_addr1)
			i+= 1
			#print("Iterations in frames for feedback:", i)




			#___USE THE CODE BELOW IF transmission view is required as well___#
			#frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
			#print ("TRANSMITTED FPS--->:		", fps)
			#cv2.imshow('TRANSMITTING VIDEO',frame)
			#____TO close the dialougue box and uae framerate___#
			'''key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				server_socket1.close()
				break'''
			if cnt == frames_to_count:
				try:
					fps = round(frames_to_count/(time.time()-st))
					st=time.time()
					cnt=0
				except:
					pass
			cnt+=1
		
		print("FPS Trasmitted:	", fps)
		print("FPS Received:	", feedback_fps)

		####rounding off client fps####
		k+=1
		
		if (k<=5):
			l += feedback_fps
		else:
			FPS = l/5
			print( "rounded off client fps", FPS )
			if (FPS<5):
				print("BAD CONNECTION")
				m+=1

			else: 
				print("OKAY-ISH connection")
				m-=1
			l, k=0, 0
		if(m>1):
			print ("count of consective bad connections: ", m)

		if (m>=5):
			print("....NEED TO CHANGE CONNECTION PARAMETERS NOW!.....")
			change = b'change'
			

			#server_socket3.sendto(str(FPS).encode('utf-8'),(client_addr3))
		#server_socket3.sendto(str(FPS).encode('utf-8'),(client_addr3))

		
			


			#print ("THE FPS DATA FROM CLIENT:", feedback_fps)

			  # to close loop after i frames

		#msg1,client_addr2 = server_socket2.recvfrom(BUFF_SIZE2)
		#print('Received from || UDP: %s', msg1)
		


