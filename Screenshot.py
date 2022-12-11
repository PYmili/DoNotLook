import pyautogui
import io
import base64
from PIL import ImageGrab, Image


def SaveScreenshot() -> bool:
    try:
        img = pyautogui.screenshot(region=[0, 0, 1920, 1080])
        img.save("./screenshot.jpg")
    except OSError:
        return False
    return True

def GetScreenshotBase64() -> str:
    try:
        img = pyautogui.screenshot(region=[0, 0, 1920, 1080])
    except OSError:
        return str(
            base64.b64encode(
                open(
                    "../image/icon/icon.png",
                    "rb"
                ).read()
            )
        ).replace("b'", "").replace("'", "")
    ImageByts = io.BytesIO()
    img.save(ImageByts, format="JPEG")
    return str(base64.b64encode(ImageByts.getvalue())).replace("b'", '').replace("'", '')

def GetImageGradBase64() -> str:
    img = ImageGrab.grab()
    ImageByts = io.BytesIO()
    img.save(ImageByts, format="JPEG")
    return str(base64.b64encode(ImageByts.getvalue())).replace("b'", '').replace("'", '')

def ScrseensByts() -> bytes:
    ImageByts = io.BytesIO()
    try:
        img = ImageGrab.grab()
    except OSError:
        img = Image.open("./image/icon/icon.png")

    img.save(ImageByts, format="JPEG")

    BytesData = ImageByts.getvalue()
    return BytesData