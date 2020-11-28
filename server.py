import socket
import sys
import os


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    #print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    #sock.listen(1)
    while True:
        #print(sys.stderr, 'waiting for a connection')
        #client_connection, client_address = sock.accept()
        try:
            #print(sys.stderr, 'connection from', client_address)
            while True:
                #data = client_connection.recv(1000)
                #print(sys.stderr, 'received "%s"' % data)
                data = "hi"
                if data:
                    #### TODO: insert the correct variables ####
                    client_send = "GET index.html HTTP/1.1\r\n...\r\nConnection: close\r\n...\r\n\r\n"
                    client_send_lines = client_send.split('\r\n')
                    file_name = client_send_lines[0].split()[1]
                    content_file = open(file_name, "r").read()
                    length = os.stat(file_name).st_size
                    connection = ""
                    for line in client_send_lines:
                        if line.startswith("Connection: "):
                            connection = line.split()[1]
                    good_response = "HTTP/1.1 200 OK\nConnection: " + connection + "\nContent-Length: " + str(length)+"\r\n\r\n"
                    response = good_response + content_file
                    print(response)
                    #client_connection.send(response)
                    if connection == "close":
                        x=5
                        #client_connection.close()
                    elif connection == "keep-alive":
                        x=5




                else:
                    #print(sys.stderr, 'no more data from', client_address)
                    break
        finally:
            x=5
            #connection.close()




if __name__ == "__main__":
    main()