import socket
from shared.constants import SOCKET_TIMEOUT, DEFAULT_PORT
import threading


class ServerManager:

    def __init__(self, host: str = None, port: int = DEFAULT_PORT, lock=None):
        self.host = host or self._get_private_ip()
        self.port = port
        self.server_socket = None
        self.client_connections = []
        self._is_binded = False
        self._stop_event = threading.Event()
        self.lock = lock


    def start(self):
        try:
            self.thread = threading.Thread(
                target=self.run,
                name="Listening Server",
                daemon=True,
            )
            self.thread.start()
    
        except KeyboardInterrupt:
            self.stop_event.set()

    def run(self):

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        #This is for changing the option of socket at socket level or tcp connection level.
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, # Describe Level -> SOL_SOCKET is level name
            socket.SO_REUSEADDR, # What to change -> Reuse Address
            1, # 1->Enable, 0->Disable
        )

        while not self._is_binded:
            try:
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen(3)
                self.server_socket.settimeout(1.0)
                self._is_binded = True

            except OSError:
                print("Port Changing")
                self.port += 1
            except KeyboardInterrupt:
                print("ClipSync Has Stopped...")
                self.close()

        try:
            while not self._stop_event.is_set():

                try:
                    if len(self.client_connections) < 1:
                        client_connection, address = self.server_socket.accept()
                        self.client_connections.append((client_connection, address,))
                        print(f"Connection Established Suncessfully With {address[0]}:{address[1]}")

                except socket.timeout:
                    continue
                except OSError:
                    self._stop_event.set()
                except KeyboardInterrupt:
                    self._stop_event.set()

        except KeyboardInterrupt:
            pass

        finally:
            self.close()


    def close(self) -> None:
        self._stop_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass

        print("ClipSync Server Is Stopped")


    def close_client(self) -> None:
        conn = self.client_connections.pop()
        conn[0].close()



    def _get_private_ip(self) -> str:

        getIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't actually send data, just finds the interface used for external traffic
            getIp.connect(("8.8.8.8", 80))
            ip = getIp.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"  # fallback
        finally:
            getIp.close()
        return ip


