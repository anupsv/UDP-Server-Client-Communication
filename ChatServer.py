import socket
import sys


class UDP_Socket_Server:

    # class init function is used to create a socket of type Datagram.
    def __init__(self, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            print 'Failed to create socket on the machine.'
            sys.exit()

        # this is the tupe of the server address and the port.
        # instead of hardcoding the localhost ip, we are querying the IP of the hostname of the system and connect
        # to the IP pointed by it.
        server_address_tuple = (self.get_ip_address(), port)
        print 'starting up on {}'.format(server_address_tuple)

        # We try to bind on the server host and port specified.
        try:
            self.sock.bind(server_address_tuple)
        except:
            print 'Failed to bind socket on the Port :'.format(port)
            sys.exit()

        # Set of sockets that sent GREETING messages.
        self.client_socket_list = set()

    # This is used to query which interface is being used for the IP and returns the IP.
    # We will be querying DNS of Google i.e 8.8.8.8
    def get_ip_address(self):
        # Create a datagram for DNS request
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # As per specifications
        _host = "8.8.8.8"
        _port = 80
        s.connect((_host, _port))
        # Return the first element of the array.
        return s.getsockname()[0]

    # this function is the main function for listening for data from the clients and also
    # handles the forwarding mechanism
    def listen_on_port(self):
        while True:

            # Here we try to receive data from the socket, a total of 4096 bytes.
            try:
                data, address = self.sock.recvfrom(4096)
            except:
                print 'Failed to receive using the socket'
                sys.exit()

            print 'Received input {} bytes from {} : {}'.format(len(data), address, data)

            # Here we check to follow the required protocol methods.
            # If the message type is greeting, we understand that the client is new and add it to the list of clients
            # to forward messages.
            if data == "GREETING":
                print "Greeting detected, Adding host {} to list.......".format(str(address[0]))
                self.client_socket_list.add(address)

            # If the data starts with "MESSAGE", then we know that this is data sent from client which needs to be
            # forwarded to all the clients.
            if data.startswith("MESSAGE", 0, 7):

                # Here we loop over the different clients in the list and forwarded the message to all of them,
                # including the client from which it was received from.
                for _client in self.client_socket_list:
                    # print "Sending message to client {}:{}".format(address[0],address[1])
                    tosend = "<-INCOMING From <{}:{}> : {}".format(address[0], address[1], data[8:])

                    # Here we try to send the message to each client looping over the list. _client is a tuple as
                    # needed for the sendto function.
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
