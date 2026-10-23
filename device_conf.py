import json
import socket
import uuid
from pathlib import Path
from application_config_data import DEFAULT_TCP_PORT

CONFIG_PATH = Path(__file__).resolve().parent / "device_config.json"


def load_or_create_device_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)

    device = {
        "device_id": str(uuid.uuid4()),
        "device_name": socket.gethostname(),
        "tcp_port": DEFAULT_TCP_PORT,
        "protocol_version": 1,
    }

    save_device_config(device)
    return device


def save_device_config(device):
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(device, file, indent=4)

