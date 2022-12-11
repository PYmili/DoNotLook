import io
import os
import socket

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox

from PIL import Image

import Screenshot

def GetIP():
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Socket.connect(('8.8.8.8', 80))
    __ip = Socket.getsockname()[0]
    Socket.close()
    return __ip

class DisplayTread(QThread):
    def __init__(self, label):
        super(DisplayTread, self).__init__()
        self.label = label
        self.IS = True

    def run(self) -> None:
        self.label.setStyleSheet(
            """
            background-color: white;
            """
        )
        while self.IS:
            ImageByts = Screenshot.ScrseensByts()
            if ImageByts:
                File = Image.open(io.BytesIO(ImageByts)).resize((
                    self.label.width(),
                    self.label.height()
                ))
                File.save("./image/login/log.jpg")
                Pixmap = QPixmap("./image/login/log.jpg")
                self.label.setPixmap(Pixmap)
                self.label.setAlignment(Qt.AlignCenter)
                # time.sleep(1)
            else:
                break

    def stop(self):
        self.IS = False
        self.quit()
        self.wait()
        print("Exit DisplayThread")

class NetworkServerThread(QThread):
    def __init__(self):
        super(NetworkServerThread, self).__init__()

    def run(self) -> None:
        os.popen(f"start ./bin/NetworkServer/NetworkServer.exe")
        # while self.IS:
        #     NetworkServer.Server((f'{GetIP()}', 8002)).SendScreenshot()
        #     print(f"[{GetIP()}:8002] [True]")

    def __del__(self):
        self.IS = False
        self.wait()

    def stop(self):
        os.popen("TASKKILL /F /IM NetworkServer.exe")
        self.quit()
        self.wait()
        print("Exit NSThread")


class main(QWidget):
    def __init__(self):
        super(main, self).__init__()

        self.Ns = False

        self.Qtime = QTimer()

        self.resize(960, 540)
        self.setWindowTitle("DoNotLook")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("./image/icon/icon.png"))
        self.Header()
        self.UI()

    def UI(self):
        Bg = QLabel(self)
        Bg.setPixmap(QPixmap("./image/bg.png"))
        Bg.setGeometry(0, 0, self.width(), self.height())
        Bg.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        HOST = QLabel(f"{GetIP()}", self)
        HOST.setGeometry(int((960 - 120) / 2), 0, 120, 20)
        HOST.setStyleSheet("""
            font-size: 15px;
            color: yellow;
        """)

        self.LeftQWidget = QWidget()
        self.LeftUI()

        self.RightQWidget = QWidget()
        self.Home()
        self.Connect()

        self.MainLayout = QHBoxLayout()
        self.MainLayout.addWidget(self.LeftQWidget, 1)
        self.MainLayout.setSpacing(0)
        self.MainLayout.addWidget(self.RightQWidget, 10)

        self.UpAndDownLayout = QVBoxLayout(self)
        self.UpAndDownLayout.addWidget(self.HeaderQWidget, 1)
        self.UpAndDownLayout.addLayout(self.MainLayout, 10)

        self.Widgets = {
            0 : self.RightQWidget,
            1 : self.HomeWidget,
            2 : self.ConnectWidget
        }

    def LeftUI(self):
        self.ButtonStyle = """
            QPushButton {
                font-size: 20px;
                background-color: #4d4848;
                color: white;
                border:2px groove gray;
                border-radius: 10px;
                padding: 2px 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: white;
                color: #000000;
            }
        """
        self.CheckButtonStyle = self.ButtonStyle.replace("color: white;", "color: #000000;")

        self.HOME = QPushButton("Home", self.LeftQWidget)
        self.HOME.setStyleSheet(self.ButtonStyle)
        self.HOME.setGeometry(0, 0, 85, 40)
        self.HOME.clicked.connect(self.SetHomeWidget)

        self.ConnectButton = QPushButton("Connect", self.LeftQWidget)
        self.ConnectButton.setStyleSheet(self.ButtonStyle)
        self.ConnectButton.setGeometry(0, 40, 85, 40)
        self.ConnectButton.clicked.connect(self.SetConnectWidget)

        self.Buttons = {
            0 : self.HOME,
            1 : self.ConnectButton
        }

    def DellWidgets(self, args: dict):
        for i in args.values():
            # self.MainLayout.removeWidget(i)
            i.hide()

    def ShowButtons(self, args: dict):
        for i in args.values():
            i.setEnabled(True)
            i.setStyleSheet(self.ButtonStyle)

    def SetHomeWidget(self):
        self.Widgets.pop(1)
        self.DellWidgets(self.Widgets)
        self.Buttons.pop(0)

        self.HOME.setEnabled(False)
        self.ShowButtons(self.Buttons)

        self.MainLayout.addWidget(self.HomeWidget, 10)
        self.Widgets[1] = self.HomeWidget
        self.Buttons[0] = self.HOME

        self.HomeWidget.show()
        self.HOME.setStyleSheet(self.CheckButtonStyle)

    def NetWorkRun(self):
        self.Ns = NetworkServerThread()
        self.DisplayLabel.show()
        self.DisplayTh = DisplayTread(self.DisplayLabel)

        self.Ns.start()
        self.DisplayTh.start()
        self.RadioBroadcastButton.setEnabled(False)
        self.RadioBroadcastStopButton.setEnabled(True)


    def NetWorkStop(self):
        self.DisplayTh.stop()
        self.Ns.stop()

        self.DisplayLabel.hide()
        self.RadioBroadcastButton.setEnabled(True)
        self.RadioBroadcastStopButton.setEnabled(False)

    def Home(self):
        self.HomeWidget = QWidget()

        self.DisplayLabel = QLabel(self.HomeWidget)
        self.DisplayLabel.setGeometry(10, 50, 850, 420)

        self.RadioBroadcastButton = QPushButton("开启共享屏幕", self.HomeWidget)
        self.RadioBroadcastButton.clicked.connect(self.NetWorkRun)
        self.RadioBroadcastButton.setGeometry(10, 10, 80, 40)
        self.RadioBroadcastButton.setStyleSheet("""
            QPushButton {
                background-color: green;
                border:2px groove gray;
                border-radius: 10px;
                padding: 2px 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: white;
                color: #000000;
            }
        """)

        self.RadioBroadcastStopButton = QPushButton("关闭共享屏幕", self.HomeWidget)
        self.RadioBroadcastStopButton.clicked.connect(self.NetWorkStop)
        self.RadioBroadcastStopButton.setGeometry(100, 10, 80, 40)
        self.RadioBroadcastStopButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                border:2px groove gray;
                border-radius: 10px;
                padding: 2px 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: white;
                color: #000000;
            }
        """)
        self.RadioBroadcastStopButton.setEnabled(False)

    def SetConnectWidget(self):
        self.Widgets.pop(2)
        self.DellWidgets(self.Widgets)
        self.Buttons.pop(1)

        self.ConnectButton.setEnabled(False)
        self.ShowButtons(self.Buttons)

        self.MainLayout.addWidget(self.ConnectWidget, 10)
        self.Widgets[2] = self.ConnectWidget
        self.Buttons[1] = self.ConnectButton

        self.ConnectWidget.show()
        self.ConnectButton.setStyleSheet(self.CheckButtonStyle)

    def HostButtonEvnet(self) -> None:
        Text, statuc = QInputDialog.getText(self.ConnectWidget, "Connect Host", "Input Host")
        if len(Text) != 0:
            os.popen(f"start./bin/DoNotLookDisplay/DoNotLookDisplay.exe -i={Text}")
        else:
            QMessageBox.information(self.ConnectWidget, "information", "Not Input Host!")

    def Connect(self) -> None:
        self.ConnectWidget = QWidget()
        self.HostButton = QPushButton("连接其他屏幕", self.ConnectWidget)
        self.HostButton.setGeometry(10, 10, 80, 40)
        self.HostButton.clicked.connect(self.HostButtonEvnet)
        self.HostButton.setStyleSheet("""
            QPushButton {
                background-color: white;
                border:2px groove gray;
                border-radius: 10px;
                padding: 2px 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #000000;
            }
        """)

    def Header(self) -> None:
        self.HeaderQWidget = QWidget()

        self.QuitButton = QPushButton(self.HeaderQWidget)
        self.QuitButton.setIcon(QIcon("./image/quit.png"))
        self.QuitButton.setIconSize(QSize(40, 40))
        self.QuitButton.setGeometry(895, 1, 40, 40)
        self.QuitButton.clicked.connect(self.ExitEvent)
        self.QuitButton.setStyleSheet("""
            border:2px groove gray;
            border-radius: 20px;
            padding: 2px 4px;
        """)

        self.MinimizeButton = QPushButton(self.HeaderQWidget)
        self.MinimizeButton.setIcon(QIcon("./image/minimize.png"))
        self.MinimizeButton.setIconSize(QSize(40, 40))
        self.MinimizeButton.setGeometry(840, 1, 40, 40)
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.MinimizeButton.setStyleSheet("""
            border:2px groove gray;
            border-radius: 20px;
            padding: 2px 4px;
        """)

        self.IconButton = QLabel(self.HeaderQWidget)
        self.IconButton.setGeometry(1, 1, 100, 40)
        self.IconButton.setText("DoNotLook")
        self.IconButton.setStyleSheet("""
            color: white;
            font-size: 20px;
        """)

    def ExitEvent(self) -> None:
        if self.Ns != False:
            self.NetWorkStop()
        self.close()

    def mouseMoveEvent(self, event: QMouseEvent):
        self._endPos = event.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            self._isTracking = True
            self._startPos = QPoint(event.x(), event.y())
        elif event.button() == Qt.MidButton:
            self._isTracking = False
        else:
            self._isTracking = False

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec()