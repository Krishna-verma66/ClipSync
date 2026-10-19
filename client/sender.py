from .clipboard import ClipboardManager
from shared.constants import CLIPBOARD_POLL_INTERVAL, MAX_MESSAGE_SIZE
import time
from shared.schemas import ClipboardUpdateMessage
from uuid import uuid4


clipboard = ClipboardManager()

def clipboard_message_formation(text):
    message = ClipboardUpdateMessage(device_id=uuid4(), content=text)

    bytedata = message.model_dump_json().encode("utf-8")
    return bytedata



def sendData(connection, stop_event):

    while not stop_event.is_set():
        try:
            textdata = clipboard.get_clipboard_update()

            if textdata is not None:
                
                connection.sendall(clipboard_message_formation(textdata))

            time.sleep(CLIPBOARD_POLL_INTERVAL)
        except Exception:
            break

        