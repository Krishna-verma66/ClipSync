from .clipboard import ClipboardManager
from shared.constants import CLIPBOARD_POLL_INTERVAL, MAX_MESSAGE_SIZE
from shared.schemas import ClipboardUpdateMessage
from uuid import uuid4
import threading
from device_conf import load_or_create_device_config


class SenderManager:
    def __init__(self, my_device, connection, stop_event):
        self.clipboard_manager = ClipboardManager()
        self.connection = connection
        self.stop_event = stop_event
        self.my_device = my_device

    def start(self):
        try:
            self.thread = threading.Thread(
                target=self.run,
                name="Clipboard Sender Thread",
                daemon=True,
            )
            self.thread.start()
        
        except KeyboardInterrupt:
            self.stop_event.set()

    def run(self):

        while not self.stop_event.is_set():
            try:
                textdata = self.clipboard_manager.get_clipboard_update()

                if textdata is not None:
                    bytedata = self.clipboard_message_formation(textdata)
                    self.connection.sendall(bytedata)

            except Exception as ex:
                break

    def clipboard_message_formation(self, text):
        message = ClipboardUpdateMessage(
            message_id=str(uuid4()), 
            device_id=self.my_device["device_id"],
            content=text
        )
        bytedata = message.model_dump_json().encode("utf-8")
        return bytedata



    

        