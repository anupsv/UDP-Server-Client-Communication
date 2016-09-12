import socket
import sys
from optparse import OptionParser


class UDP_Socket_Server:

    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', port)
        print 'starting up on %s port {}'.format(server_address)
        self.sock.bind(server_address)
        self.sockets = set()

    def listen_on_port(self):
        while True:
            data, address = self.sock.recvfrom(4096)

            print 'Received input {} bytes from {} : {}'.format(len(data), address,data)
            print "address : ", address

            if data == "GREETING":
                print "adding......."
                self.sockets.add(address)

            if data.startswith("MESSAGE"):

                for tmpaddr in self.sockets:
                    print "SENDING..."
                    tosend = "INCOMING From <{}:{}> : {}".format(address[0],address[1],data[8:])
                    self.sock.sendto(tosend, tmpaddr)


if __name__ == '__main__':

    server = UDP_Socket_Server(9090)
    server.listen_on_port()
    if len(sys.argv) != 3:
        print "Insufficient Parameters passed. Please check again."
        exit()
    elif int(sys.argv[2]) <= 0:
        print "Weird port detected. Please Check the port number."
        exit()

    port = int(sys.argv[2])
    server = UDP_Socket_Server(port)