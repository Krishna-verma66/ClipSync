from .clipboard import ClipboardManager
from pydantic import ValidationError
from shared.constants import CLIPBOARD_POLL_INTERVAL, MAX_MESSAGE_SIZE
from shared.schemas import ClipboardUpdateMessage
import socket
import threading




class ReceiverManager:

    def __init__(self, connection, stop_event):
        self.clipboard_manager = ClipboardManager()
        self.connection = connection
        self.stop_event = stop_event


    def start(self):
        try:
            self.thread = threading.Thread(
                target=self.run,
                name="Clipboard Sender Thread",
                daemon=True
                )
            self.thread.start()

        except KeyboardInterrupt:
            self.stop_event.set()


    def run(self):
        while not self.stop_event.is_set():
            try:
                message_bytes = self.connection.recv(MAX_MESSAGE_SIZE)
                message_dict = self.validate_message(message_bytes)

                if (message_dict is not None) and message_dict["type"] == "clipboard_update":
                    content = message_dict.get("content", None)

                    if content is not None and self.clipboard_manager.is_new_data(content):
                        self.clipboard_manager.write_clipboard(content)

            except socket.timeout:
                pass

            except Exception as ex:
                self.stop_event.set()



    def validate_message(
        self,
        raw_data: bytes,
    ) -> dict | None:
        try:
            message = ClipboardUpdateMessage.model_validate_json(
                raw_data
            )
            return message.model_dump()

        except ValidationError as exc:
            return None


