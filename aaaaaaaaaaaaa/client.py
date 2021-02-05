import socket
import protocol
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 9090))

for i in range(1):
    mes = {'type': 'connect'}
    mes_bit = protocol.MyProtocol.getByteStrFromData(mes)
    sock.send(mes_bit)
    data = sock.recv(10000)
    print(data)

    sleep(10)

sock.close()
