from .connection import ClientConnection
from .reciever import recieveData
from .sender import sendData
import argparse
import threading

def main():
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


if __name__ == "__main__":
    main()    
    