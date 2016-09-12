import socket
import sys
import select

class UDP_Socket_Client:

    def __init__(self,serverIp,serverPort):

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create message sending socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        self.server_address = (serverIp, serverPort)

    def greetServer(self):

        try:
            greetMsg = "GREETING"
            self.sock.sendto(greetMsg, self.server_address)

        except:
            print 'ERROR : Could not send "GREETING" to server. Exiting now.'
            self.sock.close()
            exit()

    def msgSendingReceivingService(self):

            sys.stdout.write('')
            sys.stdout.flush()
            while True:
                r, w, x = select.select([sys.stdin, self.sock], [], [])
                if not r:
                    continue
                if r[0] is sys.stdin:
                    data = raw_input()
                    try:
                        data = "MESSAGE {}".format(data)
                        self.sock.sendto(data, self.server_address)

                    except socket.error, msg:
                        print 'Failed to send message to server. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                        sys.exit()

                    sys.stdout.write('')
                    sys.stdout.flush()

                else:
                    data = self.sock.recv(4096)
                    print data


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print "Insufficient Parameters passed. Please check again."
        exit()
    elif int(sys.argv[4]) <= 0:
        print "Weird port detected. Please Check the port number."
        exit()

    serverIp = sys.argv[2]
    serverPort = int(sys.argv[4])

    server = UDP_Socket_Client(serverIp, serverPort)
    server.greetServer()
    server.msgSendingReceivingService()