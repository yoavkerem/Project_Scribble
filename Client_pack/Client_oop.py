import socket

class Client:
    def __init__(self,ip,port):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # responsible for changing text color, text font and back ground color ( personal task). [1;107;97m - white, "\033[1;97;40m" - dark, "\033[1;7;97m" - light
        CLIENT_PORT = port
        CLIENT_IP = ip
        print(CLIENT_PORT)
        print(CLIENT_IP)
        print("Client is starting")
        self.my_socket.connect((CLIENT_IP, CLIENT_PORT))

    def send_request_to_server(self, request):
        """Send the request to the server. First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """
        length = str(len(request.encode('utf-8')))
        zfill_length = length.zfill(2)
        message = zfill_length + request
        self.my_socket.send(message.encode('utf-8'))

    def handle_client_response(self):
        length = self.my_socket.recv(2).decode()
        data = self.my_socket.recv(int(length)).decode()
        return data

