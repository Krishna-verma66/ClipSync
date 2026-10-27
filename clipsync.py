import threading
from device_conf import load_or_create_device_config
from Discovery.broadcaster import DeviceDiscoveryManager
from shared.extra import read_console_command, show_help
from server.connection import ServerManager
from client.connection import ClientManager 
from shared.reciever import ReceiverManager
from shared.sender import SenderManager

# make reciever and sender thread and apply pydantic 4:00 complete this



def main():
    # 1. Initialize application state
    lock = threading.Lock()
    stop_event = threading.Event()
    sync_enabled = threading.Event()
    my_device = load_or_create_device_config()
    is_connected = False


    # Device Discovery:
    discovery_manager = DeviceDiscoveryManager(
        device=my_device,
        stop_event=stop_event,
    )
    discovery_manager.start()

    #Listening Server Start:
    server_manager = ServerManager(lock=lock)
    server_manager.start()

    # client manager:
    initiate_connection = ClientManager()

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
                        if not is_connected:
                            client_socket = initiate_connection.connect(device_ip, device_port)
                            is_connected = True


                except Exception:
                    print("Enter Valid Device Number.")

            elif command == "DISCONNECT":
                if is_connected:
                    initiate_connection.closeClientConnection()
                    is_connected = False

                if len(server_manager.client_connections)>0:
                    server_manager.close_client()


            elif command == "SYNC ON":
                client_sock = None

                if sync_enabled.is_set():
                    sync_enabled.clear()

                if is_connected:
                    client_sock = client_socket
                elif len(server_manager.client_connections)>0:
                    client_sock = server_manager.client_connections[0][0]
                else:
                    print("You Are Not paired With Any Device.")
                    continue


                receiver_manager = ReceiverManager(client_sock, sync_enabled)
                sender_manager = SenderManager(my_device, client_sock, sync_enabled)
                    
                receiver_manager.start()
                sender_manager.start()
                    


            elif command == "SYNC OFF":
                if sender_manager is not None and receiver_manager is not None:
                    sync_enabled.set()

            else:
                print("-----Enter Valid Command------")
                continue

    finally:
        stop_event.set()
        sync_enabled.set()


if __name__ == "__main__":
    main()