import socket
import sys
import os


def main():
    # tcp socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(sys.argv[1]))
    sock.bind(server_address)
    sock.listen(1)
    next_request = ""
    while True:
        client_connection, client_address = sock.accept()
        try:
            # care about the client until its done
            while True:
                connection = ""
                client_sent = next_request
                #client_sent = client_connection.recv(1024).decode()
                while True:
                     client_connection.settimeout(1.0)
                     got_now = client_connection.recv(1024).decode()
                     print(got_now, end="")
                     index = got_now.find("\r\n\r\n")
                     if index != -1:
                         this_message = got_now[:index + len("\r\n\r\n")]
                         next_message = got_now[index + len("\r\n\r\n"):]

                         client_sent += this_message
                         next_request = next_message
                         break
                     else:
                         client_sent += got_now

                if client_sent:
                    client_sent_lines = client_sent.split('\n')
                    file_name = client_sent_lines[0].split()[1]

                    if file_name == "/":
                        file_name = "/index.html"
                    elif file_name == "/redirect":
                        response = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n".encode()
                        connection = "close"

                    if file_name != "/redirect":
                        file_name = file_name[1:]
                        # check if the file exist
                        if os.path.isfile(file_name):
                            length = os.stat(file_name).st_size
                            for line in client_sent_lines:
                                if line.startswith("Connection: "):
                                    connection = line.split()[1]
                            good_response = "HTTP/1.1 200 OK\nConnection: " + connection + "\nContent-Length: " + str(length) + "\r\n\r\n"
                            if file_name.endswith('.jpg') or file_name.endswith('.ico'):
                                content_file = open(file_name, "rb").read()
                                response = good_response.encode() + content_file
                            else:
                                content_file = open(file_name, "r").read()
                                response = (good_response + content_file).encode()
                        else:
                            response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode()
                            connection = "close"
                    client_connection.send(response)
                    if connection == "close" or connection == "" or length == 0 or is_empty_request(client_sent):
                        client_connection.close()
                        break
                else:
                    break
        except:
            client_connection.close()



def is_empty_request(s):
    if len(s.replace('\r\n', '').replace('\n', '').replace(' ', '')) == 0:
        return True
    return False

if __name__ == "__main__":
    main()