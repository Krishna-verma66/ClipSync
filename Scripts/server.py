from service import ServerSync

p1 = ServerSync()

try:
    p1.sendingClips()
except KeyboardInterrupt:
    print("Connection Interrupted.")
except ConnectionAbortedError:
    print("Connection Aborted")
except ConnectionResetError:
    print("Connection Closed By Client.")
finally:
    p1.closeConn()



