
# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

#buffer
BUFF_SIZE1 = 65536
BUFF_SIZE2 = 8192
BUFF_SIZE3 = 8192
##__Init Socekt 1__##
client_socket1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE1)
#___________________________________________________________________________#
##__Init Socekt 2__##
client_socket2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket2.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE2)
#___________________________________________________________________________#
##__Init Socekt 3__##
client_socket3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket3.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE3)
#___________________________________________________________________________#




host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
print(host_ip)
port1 = 9999
port2 = 9998
port3 = 9997
message1 = b'ALOHA'
quality = input("Enter quality (10-90): ")
res = input("Enter width: ")


parameter = [quality, res]
print (type(parameter), parameter)



client_socket1.sendto(message1,(host_ip,port1))

client_socket2.sendto(quality.encode('utf-8'),(host_ip,port2))
client_socket3.sendto(res.encode('utf-8'),(host_ip,port3))
#client_socket2.sendto(para,(host_ip,port2))


#client_socket2.sendto(para.encode('utf-8'),(host_ip,port2))


fps,st,frames_to_count,cnt = (0,0,20,0)
while True:
	packet,_ = client_socket1.recvfrom(BUFF_SIZE1)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
	frame = cv2.putText(frame,'RES: '+str(frame.shape),(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket1.close()
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1
	client_socket2.sendto(quality.encode('utf-8'),(host_ip,port2))
	client_socket3.sendto(res.encode('utf-8'),(host_ip,port3))
	print ("RECEIVED FPS--->:		", fps)
