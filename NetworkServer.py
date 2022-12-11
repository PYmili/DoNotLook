import socket
import Screenshot

class Server:
    def __init__(self, *args, _listen: int = 1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(*args)
        self.socket.listen(_listen)
        self.info, self.addr = self.socket.accept()

    def SendScreenshot(self) -> bool:
        Data = Screenshot.ScrseensByts()
        try:
            if self.info.send(Data):
                return True
            else:
                return False
        except ConnectionError:
            return False


def GetIP():
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.connect(('8.8.8.8', 80))
    __ip = Socket.getsockname()[0]
    Socket.close()
    return __ip

while Server((f'{GetIP()}', 8002)).SendScreenshot():
    pass
