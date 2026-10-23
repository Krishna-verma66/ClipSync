from .connection import ClientConnection
from shared.reciever import recieveData
from shared.sender import sendData
import argparse
import threading

def main(client_connections: list = None):
    if __name__ == "__main__":
        stop_event = threading.Event()
        
        try:
            #Parsing -ip address and -port from main command line argument.
            parser = argparse.ArgumentParser()
                
            parser.add_argument("--ip", "-ip", type=str)
            parser.add_argument("--port", "-port", "-p", type=int)
                
            args = parser.parse_args()
        
            #Connection Establishing with server by given ip:port.
            connection = ClientConnection(args.ip, args.port)
            client = connection.connect()
        
                #Making Threads For Sending and Getting Data.
            if client is not None:
                recieve_thread = threading.Thread(target=recieveData, args=(client,stop_event,)) 
                send_thread = threading.Thread(target=sendData, args=(client,stop_event,)) 
                            
                recieve_thread.start()
                send_thread.start()
                    
                send_thread.join()
                recieve_thread.join()
        
        except KeyboardInterrupt:
            print("Terminating...")
        except ConnectionResetError:
            print(f"Connection Is Closed By Server {connection.current_server_ip}:{connection.current_server_port}")
        finally:
            connection.closeClientConnection()
            stop_event.set()

    else:
        if client_connections is not None:
            stop_event = threading.Event()

            try:
                for client in client_connections:
                    recieve_thread = threading.Thread(target=recieveData, args=(client,stop_event,)) 
                    send_thread = threading.Thread(target=sendData, args=(client,stop_event,)) 
                                                            
                    recieve_thread.start()
                    send_thread.start()
                                                    
                    send_thread.join()
                    recieve_thread.join()
            except KeyboardInterrupt:
                stop_event.set()

            
#NOW check all files and change all code structure according to server architecture.
#Like Common interface for client that coming from server and also as client directly.
#Also make reciever.py and sender.py for both direct client and servers client.



if __name__ == "__main__":
    main()    
    