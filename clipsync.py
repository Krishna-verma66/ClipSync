import threading
from device_conf import load_or_create_device_config
from Discovery.broadcaster import DeviceDiscoveryManager
from shared.extra import read_console_command, show_help
from server.connection import ServerManager
from client.connection import ClientManager 
from shared.reciever import ReceiverManager
from shared.sender import SenderManager
from shared.connection_registry import ConnectionRegistry




def main():
    # 1. Initialize application state
    connectionregistry = ConnectionRegistry()
    lock = threading.Lock()
    stop_event = threading.Event()
    my_device = load_or_create_device_config()


    # Device Discovery:
    discovery_manager = DeviceDiscoveryManager(
        device=my_device,
        stop_event=stop_event,
    )
    discovery_manager.start()

    #Listening Server Start:
    server_manager = ServerManager(connectionregistry=connectionregistry)
    server_manager.start()

    # client manager:
    client_manager = ClientManager(connectionregistry=connectionregistry)

    #Clipboard Synchronzation Managers::
    receiver_manager: ReceiverManager = None
    sender_manager: SenderManager = None

    try:
        while not stop_event.is_set():
            command = read_console_command(lock)

            if command == "":
                print("To get information, write 'help'.")
                continue
           
            elif command == "HELP":
                show_help()
           
            elif command == "EXIT":
                break
           
            elif command == "DEVICES":
                discovered_devices = discovery_manager.get_devices()

                for device in discovered_devices:
                    print(f"Device Name: {device["device_name"]}")
                    print(f"Device ID: {device["device_id"]}")
                    print(f"Device IP: {device["ip"]}")
                    print(f"Device Listening Port: {device["tcp_port"]}")
                    print()

            elif command == "CONNECTIONS":
                for i, connection in enumerate(connectionregistry.get_all_connections()):
                    print(f"{i+1}) {connection[0]}")
 
            elif command.startswith("CONNECT"):
                lst = command.split(" ")
                discovered_devices = discovery_manager.get_devices()
                try:
                    if len(lst) == 2:
                        device_num = int(lst.pop())
                        device = discovered_devices[device_num-1]

                        device_ip = device["ip"]
                        device_port = device["tcp_port"]

                        #Socket created by clinet connection.
                        client_manager.connect(device_ip, device_port)

                except Exception:
                    print("Enter Valid Device Number.")

            elif command == "DISCONNECT":
                client_manager.closeConnection()

            elif command == "SYNC ON":
                if connectionregistry.get_connection_count() > 0:
                    receiver_manager = ReceiverManager(connectionregistry.get_all_connections()[0][1])
                    sender_manager = SenderManager(my_device, connectionregistry.get_all_connections()[0][1])

                    receiver_manager.start()
                    sender_manager.start()
                else:
                    print("You Are Not Connected To Any Device.")

            elif command == "SYNC OFF":
                if((receiver_manager is not None) and (sender_manager is not None)):
                    receiver_manager.closeReceiver()
                    sender_manager.closeSender()
                
            else:
                print("-----Enter Valid Command------")
                continue

    finally:
        stop_event.set()


if __name__ == "__main__":
    main()