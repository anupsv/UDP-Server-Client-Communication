import socket
import sys
import select


class UDP_Socket_Client:
    def __init__(self, server_ip, server_port):

        try:
            if not self.hostname_ip_exists(server_ip):
                print "The given server ip/hostname could not be found.\nHost : {}\nPort : {}\nExiting now.".format(server_ip,server_port)
                sys.exit()
        except socket.error, msg:
            print "Could not verify existance of host / IP. Exiting Now."
            sys.exit()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create message sending socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        self.server_address = (server_ip, server_port)

    # Function to check if the given hostname resolves to IP or not.
    # Even if IP is supplied gethostbyname returns output
    def hostname_ip_exists(self, ip):
        try:
            socket.gethostbyaddr(ip)
            return True
        except socket.error:
            return False

    # this function sends "GREETING" to the server as per protocol specification
    def greetServer(self):

        try:
            greetMsg = "GREETING"
            self.sock.sendto(greetMsg, self.server_address)

        except socket.error, msg:
            print 'ERROR : Could not send "GREETING" to server.\nError Code {}\nReason : {}\n Exiting now.'.format(str(msg[0]), msg[1])
            self.sock.close()
            exit()

    # This Function handles the Message sending and receiving part. It uses the stdio for input and output and
    # uses select to swtich between the input and output when needed.
    # This is select is crucial as the "raw_input" Suspends the thread until the user enters the input and any
    # Communication from the server to the client will not be seen until the input from user has been detected.
    def msgSendingReceivingService(self):

        sys.stdout.write('+>')
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
                print data + "\n+>"


if __name__ == '__main__':

    try:

        # Checking if required number of parameters are given.
        # Also checks if invalid options are submitted.
        # Adheres to Standards of linux script and exists if invalid option is supplied.
        if len(sys.argv) != 5:
            if len(sys.argv) < 5:
                print "!! ERROR !! : Insufficient Parameters passed. Please check again."
            elif len(sys.argv) > 5:
                print "!! ERROR !! : Invalid Additional Parameters detected."
            exit()

        # map all argv in dictionary for ease of access, exclude argv[0] as its the script.
        argvmap = {}
        for i in range(1, len(sys.argv), 2):
            if i == (len(sys.argv) - 1):
                continue

            argvmap[sys.argv[i]] = sys.argv[i+1]

        serverIp = argvmap["-sip"]
        serverPort = int(argvmap["-sp"])

        if int(serverPort) <= 0:
            print "Weird port detected. Please Check the port number."
            exit()

        server = UDP_Socket_Client(serverIp, serverPort)
        server.greetServer()
        server.msgSendingReceivingService()

    except KeyboardInterrupt:
        print '\nKeyBoard Interrupt Detected. Shutting down client.'
        sys.exit(0)
