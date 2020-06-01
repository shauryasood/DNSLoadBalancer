import sys
import threading
import time
import random
import socket


#client task
def client():
    # get the hostname for LS
    lsHostName = sys.argv[1]
    # get the port number to connect to the LS
    lsPortNum = int(sys.argv[2])

    filein = open("PROJ2-HNS.txt", "r+")
    fileout = open("RESOLVED.txt", "w+")

    lines = filein.readlines()
    hostNames = list()
    for line in lines:
        line = line.replace("\r", "").replace("\n", "")
        hostNames.append(line)

    for line in hostNames:
        try:
            ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[C]: Socket created to connect to LS server.")
        except socket.error as err:
            print('[C]: Socket Open Error: {} \n'.format(err))
            exit()

        ls_addr = socket.gethostbyname(lsHostName)
        ls_server_binding = (ls_addr, lsPortNum)
        ls.connect(ls_server_binding)
        print("[C]: Connected to the LS server.")

        ls.send(str(line).encode('utf-8'))

        #recv data
        data_from_server = ls.recv(500)
        temp = str(data_from_server)
        fileout.write(temp + "\n")
        print("Data written to RESOLVED.txt")

        ls.close()

    filein.close()
    fileout.close()
    exit()



# main
if _name_ == "_main_":
    t2 = threading.Thread(name='client', target=client)
    t2.start()
