import socket 
from shared.constants import SOCKET_TIMEOUT


class ClientManager:
    
    def __init__(self, connectionregistry = None):
        self.connectionregistry = connectionregistry

    def connect(self, IP_add: str = None, port: int = None):
        try:

            if(self.connectionregistry.get_connection_count() < 1):
            
                client_socket = socket.socket(
                    socket.AF_INET, 
                    socket.SOCK_STREAM
                )

                client_socket.settimeout(SOCKET_TIMEOUT)
                client_socket.connect((IP_add, port))

                self.connectionregistry.add_connection(client_socket.getpeername(), client_socket)
                print(f"Connection Established With Server {client_socket.getpeername()}")
            else:
                print(f"You Are Already Connected With {self.connectionregistry.get_all_connections()[0][0]}")

        except socket.gaierror:
            print("Invalid HostName or IP.")
            try: 
                client_socket.close()
            except OSError: 
                pass

        except ConnectionRefusedError:
            print(f"Connection Refused - Server({client_socket.getpeername()}) Not Reachable.")
            try: 
                client_socket.close()
            except OSError: 
                pass

        except socket.timeout:
            print("Connection Timed Out.")
            try: 
                client_socket.close()
            except OSError: 
                pass

        except OSError as ex:
            print(ex)
            try: 
                client_socket.close()
            except OSError: 
                pass 

        
    
    def closeConnection(self):
        try:
            if self.connectionregistry.get_connection_count() > 0:
                connection_list = self.connectionregistry.get_all_connections()
                connection = connection_list.pop()
                connection[1].close()

                connection_id = connection[0]

                removed = self.connectionregistry.remove_connection(connection_id)
                print(f"Connection Closed with {connection_id} Successfully.")
            else:
                print("You Are Not Connected To Anyone.")
        except Exception:
            print(f"There is something wrong while disconnecting to Server {connection[0]}")
        

        




