# use this to test the sockets. Start this in a terminal
# on host machine:      $ sudo python3 echo_server.py 
# On the guest machine make a cient.py file using the code in "echo_client.py". Make the necessary changes in ip adress.Keep the oprt number same.
# on guestmachine:      $ sudo python3 client.py


import socket
import cv2

def Main():
   
    host = '192.168.102.100' #Server ip
    port = 5940

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message from: " + str(addr))
        print("From connected user: " + data)
        data = data.upper()
        print("Sending: " + data)
        s.sendto(data.encode('utf-8'), addr)
    c.close()

if __name__=='__main__':
    Main()