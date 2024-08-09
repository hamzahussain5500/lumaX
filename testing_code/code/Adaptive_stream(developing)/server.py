'''localIP     = "127.0.0.1"

localPort   = 20001

bufferSize  = 2**16

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,bufferSize)
# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))'''



import cv2, imutils, socket
import numpy as np
import time
import base64



bufferSize  = 2**16
#######################__INITIALIZING THE SOCKET1__###########################
server_socket1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, bufferSize)
#############################################################################
#######################__INITIALIZING THE SOCKET2__###########################
server_socket2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket2.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, bufferSize)
#############################################################################



host_name = socket.gethostname()
print("Name of the server is {}".format(host_name))
host_ip = '127.0.0.1'                       #   socket.gethostbyname(host_name)
print("IP of the host is {}".format(host_ip))
port1 = 20001
port2 = 20002
socket_address1 = (host_ip,port1)
socket_address2 = (host_ip,port2)
print ("The adress of server is: {}".format(socket_address1))
print ("The adress of server is: {}".format(socket_address2))


    # Bind to address and ip
server_socket1.bind(socket_address1)
server_socket2.bind(socket_address2)

print("UDP server up and listening")




vid = cv2.VideoCapture(0)                   #   replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)     #   fps=0   st=0    frames_to_count=20  cnt=0   


# Listen for incoming datagrams

while(True):
    feedback,client_addr = server_socket2.recvfrom(bufferSize)    #   receive feedback from buffer

    ######################___Send Random_test_Data__#######################

    '''msgFromServer       = "Hello from the UDP server"
    bytesToSend         = str.encode(msgFromServer)
    server_socket.sendto(bytesToSend, client_addr)'''
    #_____________________________________________________________________#

    print('GOT connection from ',client_addr)

    
    
    a = 480
    b =  50
    WIDTH = a  
                                 # a is coming form the client
    t_end = time.time() + 0.08
    while time.time()<t_end:

    #while(vid.isOpened()):
		
        _,frame = vid.read()
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        server_socket1.sendto(message,client_addr)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        
        


        #cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket1.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1


    ##################__Get Feedback from the CLIENT__###################

'''
   bytesAddressPair = server_socket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

   
    # Sending a reply to client
    server_socket.sendto(bytesToSend, address)  #   sends the "Hello from the UDP server" to the client
    
'''