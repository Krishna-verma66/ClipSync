import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

#client.connect(("192.168.31.181", 5000))
client.connect(("127.0.0.1", 5000)) 
print("Device Connected Succesfully!")

copied_data = []

while len(copied_data)<6:
    data = client.recv(1024)
    data = data.decode("utf-8")
    if data != "":
        print("Received from server:", data)
        copied_data.append(data)


client.close()

