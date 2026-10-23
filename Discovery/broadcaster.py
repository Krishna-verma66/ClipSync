import socket
import threading
import time
from pydantic import ValidationError
from device_conf import load_or_create_device_config
from application_config_data import DEFAULT_BROADCAST_PORT, DISCOVERY_INTERVAL
from shared.schemas import DeviceDiscoveryMessage



class DeviceDiscoveryManager:
    def __init__(self, device, stop_event):
        self.device = device
        self.broad_port = DEFAULT_BROADCAST_PORT
        self.stop_event = stop_event
        self.announce_interval = DISCOVERY_INTERVAL

        self.devices = {}
        self.lock = threading.Lock()
        self.thread = None


    def start(self):
        try:
            self.thread = threading.Thread(
                target=self.run,
                name="ClipSync-Discovery",
                daemon=True,
            )
            self.thread.start()

        except KeyboardInterrupt:
            self.stop_event.set()


    def run(self):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            broadcast_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_BROADCAST,
                1,
            )

            broadcast_socket.bind(("", DEFAULT_BROADCAST_PORT))
            broadcast_socket.settimeout(1.0)

            next_announcement = 0.0

            while not self.stop_event.is_set():

                now = time.monotonic()

                if now >= next_announcement:
                    self.broadcast(broadcast_socket)
                    next_announcement = (now + self.announce_interval)

                try:
                    data, address = broadcast_socket.recvfrom(4096)
                    self.handle_message(data, address)

                except socket.timeout:
                    pass

                self.remove_stale_devices()

        except OSError as exc:
            if not self.stop_event.is_set():
                print(f"Discovery error: {exc}")

        except KeyboardInterrupt:
            self.stop_event.set()

        finally:
            broadcast_socket.close()
            print("Discovery stopped.")




    def broadcast(self, sock):

        try:
            message = DeviceDiscoveryMessage(
                    device_id=self.device["device_id"],
                    device_name=self.device["device_name"],
                    tcp_port=self.device["tcp_port"]
                )
            
            payload = message.model_dump_json().encode("utf-8")

            sock.sendto(
                payload,
                ("255.255.255.255", self.broad_port),
            )

        except OSError as exc:
            print(f"Announcement failed: {exc}")



    def handle_message(self, data, address):
        try:
            message = DeviceDiscoveryMessage.model_validate_json(data)
            deviceDict = message.model_dump()
        except ValidationError as ex:
            print("validation error...")
            return

        device_id = deviceDict.get("device_id")
        device_name = deviceDict.get("device_name")
        tcp_port = deviceDict.get("tcp_port")


        with self.lock:
            self.devices[device_id] = {
                "device_id": device_id,
                "device_name": device_name,
                "ip": address[0],
                "tcp_port": tcp_port,
                "last_seen": time.monotonic(),
            }


    def remove_stale_devices(self):
        now = time.monotonic()

        with self.lock:
            stale_ids = [
                device_id
                for device_id, device in self.devices.items()
                if now - device["last_seen"] > 10
            ]

            for device_id in stale_ids:
                del self.devices[device_id]


    def get_devices(self):
        with self.lock:
            return [
                device.copy()
                for device in self.devices.values()
            ]



