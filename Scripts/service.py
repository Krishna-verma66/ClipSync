import socket
import pyperclip as ppc


class ServerSync:

    def __init__(self):

        try:

            self.server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            self.server.bind(("127.0.0.1", 5000))
            self.server.listen(1)
            self.connection, self.address = self.server.accept()

            print("Assigned address and port:", self.server.getsockname())
            print("Connected Client Device:", self.address)

        except Exception:
            print("Oops! Incomming Connection Has Error...")
    
    def sendingClips(self):
        copied_data = []

        while True:
            data = ppc.paste()
            
            if data != "":
                copied_data.append(data)
                ppc.copy("")

                self.connection.sendall(data.encode("utf-8"))

    def closeConn(self):
        print("connection closed")        
        self.connection.close()
        self.server.close()