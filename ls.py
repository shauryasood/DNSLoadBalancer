import socket
import select
import sys
import threading

def ls(lsListenPort, ts1Hostname, ts1ListenPort, ts2Hostname, ts2ListenPort):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: ls server socket created")
    except socket.error as err:
        print('{}\n'.format("socket open error", err))

    server_binding = ('', int(lsListenPort))
    server.bind(server_binding)
    server.listen(1)

    host = socket.gethostname()
    print("[LS]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS]: Server IP address is {}".format(localhost_ip))
    print("\n")

    while True:
        csockid, addr = server.accept()
        print ("[LS]: Got a connection request from a client at {}".format(addr))

        data_from_client = csockid.recv(100)
        print("[LS]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

        data_from_servers = server_lookup(data_from_client, ts1Hostname, ts1ListenPort, ts2Hostname, ts2ListenPort)
        print(data_from_servers)
        csockid.send(data_from_servers)


def server_lookup(data, ts1Hostname, ts1ListenPort, ts2Hostname, ts2ListenPort):
    try:
        server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: ls server socket created")
    except socket.error as err:
        print('{}\n'.format("socket open error", err))

    server1_address = socket.gethostbyname(ts1Hostname)
    server1_binding = (server1_address, int(ts1ListenPort))
    server1.connect(server1_binding)

    try:
        server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: ls server socket created")
    except socket.error as err:
        print('{}\n'.format("socket open error", err))

    server2_address = socket.gethostbyname(ts2Hostname)
    server2_binding = (server2_address, int(ts2ListenPort))
    server2.connect(server2_binding)

    server1.send(data)
    server2.send(data)

    inputs = [server1, server2]

    while inputs:
        readable, writable, exceptional = select.select(inputs, [], [], 5)
        for s in readable:
            if s is server1:
                data = s.recv(100)
                if data:
                    print("[LS]: TS1 has returned an IP for " + data + " : " + data)
                    server1.close()
                    server2.close()
                    return data
            if s is server2:
                data = s.recv(100)
                if data:
                    print("[LS]: TS2 has returned an IP for " + data + " : " + data)
                    server1.close()
                    server2.close()
                    return data
        if not (readable or writable or exceptional):
            print("[LS]: The connections have timed out. Both TS1 and TS2 do not have the IP for: " + data)
            return data + " - Error:HOST NOT FOUND"


if _name_ == "_main_":
    ls(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])