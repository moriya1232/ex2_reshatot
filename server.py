import socket
import sys
import os



def main():
    # tcp socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(sys.argv[1]))
    sock.bind(server_address)
    sock.listen(1)
    while True:
        client_connection, client_address = sock.accept()
        try:
            while True:
                connection = ""
                #todo: set timeout
                #client_connection.settimeout(1.0)
                client_sent = client_connection.recv(1000).decode()
                #TODO: להוסיף אם אנחנו יודעים שהלקוח סיים את ההודעה רק אחרי פעמיים ירידת שורה
                print(client_sent)
                if client_sent:
                    client_sent_lines = client_sent.split('\n')
                    file_name = client_sent_lines[0].split()[1]

                    if file_name == "/":
                        file_name = "index.html"

                    if file_name == "/redirect":
                        response = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n".encode()
                        connection = "close"
                    # check if the file exist
                    elif os.path.isfile(file_name):
                        # TODO:check about it! בעצם מה שקורה לי פה זה בגלישה מהדפדפן הוא מחפש לי את שם הקובץ עם סלש בהתחלה, אחרי שנטפל בזה- למחוק את השורה
                        file_name = file_name[1:]
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
                    #TODO: לבדוק מה זה נקרא בקשות ריקות
                    if connection == "close" or connection == "" or length == 0:
                        return_the_connection = ":"
                        client_connection.close()
                        break
                else:
                    break

                #TODO: remove:
                break
        finally:
            client_connection.close()
        # TODO: remove:
        break




if __name__ == "__main__":
    main()