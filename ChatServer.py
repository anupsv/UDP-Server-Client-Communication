import socket
import sys


class UDP_Socket_Server:
    def __init__(self, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print 'Failed to create socket on the machine.'
            sys.exit()

        server_address_tuple = ('127.0.0.1', port)
        print 'starting up on {}'.format(server_address_tuple)

        try:
            self.sock.bind(server_address_tuple)
        except:
            print 'Failed to bind socket on the Port :'.format(port)
            sys.exit()

        # Set of sockets that sent GREETING messages.
        self.client_socket_list = set()

    def listen_on_port(self):
        while True:
            try:
                data, address = self.sock.recvfrom(4096)
            except:
                print 'Failed to receive using the socket'
                sys.exit()

            print 'Received input {} bytes from {} : {}'.format(len(data), address, data)

            if data == "GREETING":
                print "Greeting detected, Adding host {} to list.......".format(str(address[0]))
                self.client_socket_list.add(address)

            if data.startswith("MESSAGE", 0, 7):
                for _client in self.client_socket_list:
                    # print "Sending message to client {}:{}".format(address[0],address[1])
                    tosend = "<-INCOMING From <{}:{}> : {}".format(address[0], address[1], data[8:])
                    try:
                        self.sock.sendto(tosend, _client)
                    except:
                        print 'Failed to send data through socket.'
                        sys.exit()


if __name__ == '__main__':

    # Checking if required number of parameters are given.
    # Also checks if invalid options are submitted.
    # Adheres to Standards of linux script and exists if invalid option is supplied.
    try:
        if len(sys.argv) != 3:
            print "!! ERROR !! : Insufficient Parameters passed. Please check again."
            exit()
        elif int(sys.argv[2]) <= 0:
            print "!! ERROR !! : Weird port detected. Please Check the port number."
            exit()

        port = int(sys.argv[2])
        server = UDP_Socket_Server(port)
        server.listen_on_port()

    except KeyboardInterrupt:
        print '\nKeyBoard Interrupt Detected. Shutting down server.'
        sys.exit(0)
