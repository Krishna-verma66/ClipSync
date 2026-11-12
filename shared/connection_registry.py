import threading


class ConnectionRegistry:

    def __init__(self):
        self.connections = {}
        self.lock = threading.Lock()

    def add_connection(self, connection_id, connection):
        with self.lock:
            self.connections[connection_id] = connection

    def remove_connection(self, connection_id):
        with self.lock:
            return self.connections.pop(connection_id, None)

    def get_connection(self, connection_id):
        with self.lock:
            return self.connections.get(connection_id)

    def get_all_connections(self):
        with self.lock:
            return list(self.connections.items())

    def get_connection_count(self):
        with self.lock:
            return len(self.connections)