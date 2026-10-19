import socket 
from shared.constants import SOCKET_TIMEOUT


class ClientConnection:
    
    def __init__(self, IP_add: str, port: int):
        self.client = None
        self.current_server_ip = IP_add
        self.current_server_port = port

    def connect(self):
        try:

            self.client = socket.socket(
                socket.AF_INET, 
                socket.SOCK_STREAM
            )

            self.client.settimeout(SOCKET_TIMEOUT)
            self.client.connect((self.current_server_ip, self.current_server_port))

            print(f"Connection Establisheed With Server {self.current_server_ip}:{self.current_server_port}")

        except socket.gaierror:
            print("There is an error in ip address or not reachable.")
            self.client = None

        except ConnectionRefusedError:
            print(f"Connection Refused - Server({self.current_server_ip}) Is Not Working Or Listening On Different Port({self.current_server_port}).")
            self.client = None

        except socket.timeout:
            print("Connection TimeOut...")
            self.client = None


        return self.client
    
    
    def closeClientConnection(self):
        try:
            if self.client is not None:
                self.client.close()
                print(f"Client Disconnected Successfully From Server {self.current_server_ip}:{self.current_server_port}")
        except Exception:
            print(f"There is something wrong while disconnecting to Server {self.current_server_ip}:{self.current_server_port}")
        

        




