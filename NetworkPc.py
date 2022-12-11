import socket
import io

class SocketPc:
    def __init__(self, *agrs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(*agrs)

    def RecvByte(self, bufsize: int = 1024):
        __Data = io.BytesIO()
        while True:
            bufdata = self.socket.recv(bufsize)
            if bufdata:
                __Data.write(bufdata)
            else:
                break
        return __Data.getvalue()

    def repr_socket(self):
        return self.socket

# while True:
#     Pc = SocketPc(('192.168.0.200', 8002))
#     data = Pc.RecvByte()
#     if data:
#         print(type(data))
#     else:
#         break