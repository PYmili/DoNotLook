import io
import sys
from threading import Thread

from tkinter import Tk
from tkinter import Label
from PIL import Image, ImageTk

import NetworkPc

class Display(Tk):
    def __init__(self, *args,  _SleepTime: float = 0.001):
        super(Display, self).__init__()
        self.args = args
        self.SleepTime = _SleepTime

        self.title("{}".format(*args))
        self.iconbitmap("./image/icon/icon.ico")
        self.geometry("960x540")
        self.ImageLabel = Label(self)
        self.ImageLabel.pack()
        self.ShowImageThread()

    def ShowImage(self) -> None:
        global PohtoImage

        while True:
            try:
                ImageByts = NetworkPc.SocketPc(self.args).RecvByte()
            except ConnectionError:
                break
            if ImageByts:
                Data = Image.open(io.BytesIO(ImageByts))

                self.update()
                try:
                    PohtoImage = ImageTk.PhotoImage(Data.resize((self.winfo_width(), self.winfo_height())))
                    self.ImageLabel['image'] = PohtoImage
                except RuntimeError:
                    break
                # time.sleep(self.SleepTime)
            else:
                break

    def ShowImageThread(self) -> None:
        Thread(target=self.ShowImage).start()

    def destroy(self) -> None:
        try:
            self.NP.repr_socket().close()
        except AttributeError:
            sys.exit()
        sys.exit()

if __name__ == '__main__':
    HOST = None
    for argv in sys.argv[1:]:
        key, value = argv.split("=")
        if key == "-i":
            HOST = value
    Display(HOST, 8002).mainloop()

