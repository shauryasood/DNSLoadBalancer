import socket as mysoc
import sys


def TS(tsListenPort):
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', int(tsListenPort))
    ss.bind(server_binding)
    ss.listen(1)
    # host = mysoc.gethostname()

    while True:
        csockid, addr = ss.accept()
        data_from_LS = csockid.recv(100)

        temp = data_from_LS.decode('utf-8')
        # dnsts1 = open("../../Downloads/student/PROJI-DNSTS1.txt", "r+")
        dnsts1 = open("PROJ2-DNSTS1.txt", "r+")
        lines = dnsts1.readlines()

        # sub1 = "NS"

        for line in lines:
            if temp == line.split(' ')[0]:
                csockid.send(line.replace("\r", "").replace("\n", ""))


if __name__ == '_main_':
    TS(sys.argv[1])
