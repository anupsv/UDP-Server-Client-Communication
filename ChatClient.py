import socket
import sys
import select


class UDP_Socket_Client:
    def __init__(self, server_ip, server_port):
        try:
            if not self.hostname_ip_exists(server_ip):
                print "The given server ip/hostname could not be found.\nHost : {}\nPort : {}\nExiting now.".format(server_ip,server_port)
                sys.exit()
        except:
            print "Could not verify existance of host / IP. Exiting Now."
            sys.exit()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
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
        except:
            print 'ERROR : Could not send "GREETING" to server.\nError Code {}\nReason : {}\n Exiting now.'
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
            try:
                r, w, x = select.select([sys.stdin, self.sock], [], [])
            except KeyboardInterrupt:
                print '\nKeyBoard Interrupt Detected. Shutting down client.'
                sys.exit(0)
            except:
                print "Python select threw error switching between std i/o and socket connection. Please check"
                sys.exit()
            if not r:
                continue
            if r[0] is sys.stdin:

                data = raw_input()
                try:
                    data = "MESSAGE {}".format(str(data))
                    #print " LEN : ", len(data)
                    self.sock.sendto(data, self.server_address)

                except:
                    print 'Failed to send message to server.'
                    sys.exit()

                sys.stdout.write('')
                sys.stdout.flush()

            else:
                try:
                    data = self.sock.recv(4096)
                except:
                    print "Failed to receive on the socket from the server"
                print data + "\n+>"


if __name__ == '__main__':

    def usage():
        print "\nUSAGE : \n\t-sip : Server IP Address\n\t-sp : Server Port."

    try:
        # Checking if required number of parameters are given.
        # Also checks if invalid options are submitted.
        # Adheres to Standards of linux script and exists if invalid option is supplied.
        if len(sys.argv) != 5:
            if len(sys.argv) < 5:
                print "!! ERROR !! : Insufficient Parameters passed. Please check again."
            elif len(sys.argv) > 5:
                print "!! ERROR !! : Invalid Additional Parameters detected."
            usage()
            exit()

        # map all argv in dictionary for ease of access, exclude argv[0] as its the script.
        argvmap = {}
        for i in range(1, len(sys.argv), 2):
            if i == (len(sys.argv) - 1):
                continue

            argvmap[sys.argv[i]] = sys.argv[i+1]

        if "-sip" not in argvmap:
            print "!! ERROR !! : Server IP required. '-sip' command line option."
            usage()
            sys.exit()
        elif "-sp" not in argvmap:
            print "!! ERROR !! : Server port required. '-sp' command line option."
            usage()
            sys.exit()

        serverIp = argvmap["-sip"]

        try:
            serverPort = int(argvmap["-sp"])
        except:
            print "Server port input was not integer, Please enter correct port number between 1024-65535."
            sys.exit()

        if int(serverPort) <= 0 or serverPort > 65535:
            print "Weird port detected. Please Check the port number."
            exit()

        server = UDP_Socket_Client(serverIp, serverPort)
        server.greetServer()
        server.msgSendingReceivingService()

    except KeyboardInterrupt:
        print '\nKeyBoard Interrupt Detected. Shutting down client.'
        sys.exit(0)
