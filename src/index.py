from src.wot_controller import WotController
from src.ocr import OCR
from src.replay import Replay

WotController.init('C:\\Games\\World_of_Tanks_EU', 'WorldOfTanks.exe')
OCR.init('C:\\Program Files\\Tesseract-OCR\\tesseract.exe')

replay_path = "C:\\Users\\Gabriel Hamel\\Documents\\wot\\bot-replay\\assets\\replay.wotreplay"
replay = Replay(replay_path)

replay.launch()
replay.wait_until_end()
