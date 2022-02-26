import psutil
from subprocess import Popen
from os import path
import pyautogui
import numpy as np
import time
import pygetwindow as gw
import signal

class WotProcess:
    def __init__(self, psutil_process):
        self.__process = psutil_process
        self.__alive = True
        signal.signal(signal.SIGINT, self.kill)

    def wait_until_closed(self):
        psutil.wait_procs([self.__process])

    def kill(self, sig = None, frame = None):
        self.__process.kill()
        self.__alive = False

    @property
    def alive(self):
        return self.__alive

class WotController:
    __game_path = ''
    __executable_name = ''
    __executable_path = ''

    def __init__(self):
        self.__window = None
        self.__region=(0, 0, 0, 0)
        self.__process = None

    @classmethod
    def init(cls, game_path: str, executable_name: str):
        cls.__game_path = game_path
        cls.__executable_name = executable_name
        cls.__executable_path = path.join(cls.__game_path,  cls.__executable_name)

    def __kill_all(self, sig = None, frame = None):
        self.__window = None
        for proc in psutil.process_iter():
            if proc.name() == self.__executable_name:
                proc.kill()

    def play_replay(self, replay_path) -> WotProcess:
        self.__kill_all()
        process = Popen([self.__executable_path, replay_path])
        exit_code = process.wait()
        if exit_code != 0:
            raise Exception(f'Error: Replay exited with code {exit_code}')
        wot_proc = None
        for proc in psutil.process_iter():
            if proc.name() == self.__executable_name:
                wot_proc = proc
                break
        if wot_proc == None:
            raise Exception(f'Error: Unable to attach process')
        # Attach the window
        s_waited = 0
        while s_waited < 20:
            windows = gw.getWindowsWithTitle('W.o.T. Client')
            if len(windows) == 1:
                print("Found wot window")
                break
            elif len(windows) > 1:
                raise Exception('To much WoT windows')
            time.sleep(1)
            s_waited += 1
        self.__window = windows[0]
        print(self.__window)
        self.__window.activate()
        self.__region=(self.__window.left,
                        self.__window.top,
                        self.__window.width,
                        self.__window.height)
        self.__process = WotProcess(wot_proc)
        return self.__process

    def get_region(self):
        return self.__region

    def get_current_frame(self):
        img = pyautogui.screenshot(region=self.__region)
        frame = np.array(img)
        return frame
