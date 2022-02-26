from src.ocr import OCR
from src.wot_controller import WotController
import time

class Replay:
    def __init__(self, replay_path: str):
        self.__path = replay_path
        self.__process = None
        self.__ctrl = None
        self.__ocr = None

    def launch(self):
        self.__ctrl = WotController()
        self.__process = self.__ctrl.play_replay(self.__path)
        self.__ocr = OCR(self.__ctrl.get_region()[2])

    def wait_until_end(self):
        while True:
            time.sleep(1)
            frame = self.__ctrl.get_current_frame()
            try:
                timer = self.__ocr.get_timer(frame)
                print(timer)
            except Exception as err:
                print("no timer", err)
                continue
        self.__process.wait_until_closed()
