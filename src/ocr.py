import cv2
import pytesseract
import re

class OCR:
    @classmethod
    def init(cls, tesseract_path: str):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def __init__(self, width):
        self.__y1 = 6
        self.__y2 = 23
        self.__x1 = int(0.996875 * width - 51.0)
        self.__x2 = int(width - 14)

    def get_timer(self, frame):
        cropped_frame = frame[self.__y1:self.__y2, self.__x1:self.__x2]
        timer_gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        _, thresh1 = cv2.threshold(timer_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        text = pytesseract.image_to_string(thresh1, lang='eng', config='--psm 6')
        text = text.strip()
        text = re.sub(r'[^0-9]', '', text)
        if len(text) != 4:
            raise Exception('Unable to read timer')
        minutes = int(text[:2])
        seconds = int(text[2:])
        return minutes * 60 + seconds
