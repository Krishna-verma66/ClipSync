
# shared/constants.py

# ==========================================
# Protocol
# ==========================================

PROTOCOL_VERSION = 1

# ==========================================
# Message types
# ==========================================

MSG_CONNECT = "connect"
MSG_CONNECT_ACK = "connect_ack"

MSG_CLIPBOARD_UPDATE = "clipboard_update"
MSG_ACK = "ack"
MSG_ERROR = "error"

# ==========================================
# Network defaults
# ==========================================

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000

SOCKET_TIMEOUT = 10.0
SOCKET_BACKLOG = 5

# ==========================================
# Message limits
# ==========================================

MAX_MESSAGE_SIZE = 1_048_576  # 1 MiB

# ==========================================
# Clipboard monitoring
# ==========================================

CLIPBOARD_POLL_INTERVAL = 0.5  # seconds

# ==========================================
# Connection statuses
# ==========================================

CONNECTION_CONNECTING = "connecting"
CONNECTION_CONNECTED = "connected"
CONNECTION_DISCONNECTED = "disconnected"
CONNECTION_FAILED = "failed"
