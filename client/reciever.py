from .clipboard import ClipboardManager
from pydantic import ValidationError
from shared.constants import CLIPBOARD_POLL_INTERVAL, MAX_MESSAGE_SIZE
from shared.schemas import ClipboardUpdateMessage
import time
import socket


clipboard = ClipboardManager()

# def check_incomming_data(data: bytes):
#     content = ""
#     try:
#         message = ClipboardUpdateMessage.model_validate_json(data.decode("utf-8"))
#         content = message.content
#     except ValidationError as e:
#         print("There are some validation issue in incomming message...")
#         content = None

#     return content




def recieveData(connection, stop_event):
    
    while not stop_event.is_set():
        try:
            bytedata = connection.recv(MAX_MESSAGE_SIZE)
            textdata = bytedata.decode("utf-8")
            # textdata = check_incomming_data(bytedata)

            if textdata is not None and textdata != "" and clipboard.is_new_data(textdata):
                clipboard.write_clipboard(textdata)

            time.sleep(CLIPBOARD_POLL_INTERVAL)

        except socket.timeout:
            pass

        except Exception:
            break
        
        
        
        
        
    


